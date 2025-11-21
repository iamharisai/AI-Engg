from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()



response = client.responses.create(
    model="gpt-5",
    input="Tell me a joke about programmers in one sentence."
)

print(response.output_text)