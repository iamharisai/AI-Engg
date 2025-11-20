import requests
import os
from dotenv import load_dotenv

load_dotenv()

uri = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
}

payload = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": "user",
            "content": "Why should I use AI for software development? answer in one word"
        }
    ]
}

response = requests.post(uri, headers=headers, json=payload)
print(response.json()["choices"][0]["message"]["content"])