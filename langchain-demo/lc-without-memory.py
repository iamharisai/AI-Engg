from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI() # default 'model_name': 'gpt-3.5-turbo-0125'
prompt = ChatPromptTemplate.from_template("tell me a joke about {foo}")
parser = StrOutputParser()

while True:
    user_text = input("You: ")
    if user_text.lower() in ["exit", "quit", "bye"]:
        break
    prompt = ChatPromptTemplate.from_template(user_text)
    chain = prompt | model | parser

    answer = chain.invoke({})
    print("AI: " + answer)

# There will be no memory here

# You: hello
# Hello! How can I assist you today?
# You: what is python
# Python is a high-level, interpreted programming language known for its simplicity and readability. 
# You: what is pip in one line
# Pip is a package manager for installing and managing Python packages.
# You: how they both are connected?
# They are connected through their function in the body. The brain controls and coordinates all bodily functions, including those related to the nervous system, while the heart pumps blood throughout the body, delivering oxygen and nutrients to all the organs, including the brain. Additionally, the brain sends signals to the heart to regulate its beating and the heart sends signals to the brain through hormones and nerve signals. Overall, they work together to ensure the body functions properly and efficiently.
# You: bye