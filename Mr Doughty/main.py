import os
from anthropic import Anthropic
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.environ.get("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)

prompt = "create a 5 question mcq for this, strictly about the content covered in the lesson {NO PREAMBLE}. put each question into numbered xml tag <question_#></question_#> and the multiple choice options into corresponding numbered xml tag <Answers_#></Answers_#> can you also tag the correct answer and the wrong answers and nest each question separately "


# Make sure the prompt and user input are properly formatted

# Send the formatted content to Claude for analysis
def response():
    word = input("Enter a clean transcript: ")
    content = f"{prompt} {word}"

    message = client.messages.create(
        max_tokens=4000,
        messages=[
            {"role": "user", "content": content}
        ],
        model="claude-2.1",
    )
    print("debug message: ", message)
    return message


def format_mcq(content):
    formatted_result = "<h2>Analysis Result:</h2>"

    for block in content:
        if block['type'] == 'text':
            formatted_result += "<p>" + block['text'].replace('\n', '<br>') + "</p>"
        elif block['type'] == 'multiple_choice_question':
            formatted_result += "<form>"
            formatted_result += "<div class='question'>"
            formatted_result += f"<p><strong>{block['question']}</strong></p>"
            for i, option in enumerate(block['Answers'], start=1):
                is_correct = 'correct' if option['correct'] else 'wrong'
                formatted_result += f"<input type='radio' id='question{block['question_number']}_{i}' name='question{block['question_number']}' value='{chr(96 + i)}'>"
                formatted_result += f"<label for='question{block['question_number']}_{i}' class='{is_correct}'>{chr(96 + i)}) {option['answer']}</label><br>"
            formatted_result += "</div>"
            formatted_result += "</form>"

    return formatted_result


formatted = format_mcq(response().content)
print('debug formatted output', formatted)


