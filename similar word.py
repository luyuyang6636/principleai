import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
client = Anthropic(api_key=anthropic_api_key)

def generate_similar(keyword):

  message = client.messages.create(
    max_tokens=80,
    messages=[
      {"role": "user", "content": f"Given the keyword {keyword}, can you find 5 words with exact or similar meaning to the keyword to help secondary school students understand the keyword? For example, for the word biome, similar words would be echosystem type or habitat. The structure of your output should just be words seperated by commas, nothing else"
       }
    ],
    model="claude-2.1",
  )

  response = message.content[0].text

  return response

print(generate_similar("tropical rainforest"))