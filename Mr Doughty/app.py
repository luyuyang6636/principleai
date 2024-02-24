from flask import Flask, render_template, request
import os
from anthropic import Anthropic
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    word = request.form['transcript']
    prompt = "create a 5 question mcq for this, strictly about the content covered in the lesson {NO PREAMBLE}. put each question into numbered xml tag <question_#></question_#> and the multiple choice options into corresponding numbered xml tag <Answers_#></Answers_#> can you also tag the correct answer and the wrong answers and nest each question separately "
    content = f"{prompt} {word}"

    message = client.messages.create(
        max_tokens=4000,
        messages=[
            {"role": "user", "content": content}
        ],
        model="claude-2.1",
    )

    print("Debug: Message =", message)  # Add this line for debugging

    # Check the structure of the message and adjust accordingly
    result = format_mcq(message.content)
    return render_template('index.html', result=result, content=message.content)




def format_mcq(content):
    formatted_result = "<h2>Analysis Result:</h2>"

    # Access the first item in the list, which is a ContentBlock object
    block = content[0]

    if block.type == 'text':
        formatted_result += "<p>" + block.text.replace('\n', '<br>') + "</p>"
    elif block.type == 'multiple_choice_question':
        formatted_result += "<form>"
        formatted_result += "<div class='question'>"
        formatted_result += f"<p><strong>{block.question}</strong></p>"
        formatted_result += f"<label for='question{block.question_number}'>Select an answer:</label>"
        for i, option in enumerate(block.options, start=1):
            formatted_result += f"<input type='radio' id='question{block.question_number}{chr(96 + i)}' name='question{block.question_number}' value='{chr(96 + i)}'>"
            formatted_result += f"<label for='question{block.question_number}{chr(96 + i)}'>{chr(96 + i)}) {option}</label><br>"
        formatted_result += "</div>"
        formatted_result += "</form>"

    return formatted_result


if __name__ == '__main__':
    app.run(debug=True)

