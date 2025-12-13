from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI() # default 'model_name': 'gpt-3.5-turbo-0125'
prompt = ChatPromptTemplate.from_template("tell me a joke about {foo}")
parser = StrOutputParser()

chain = prompt | model | parser

answer = chain.invoke({"foo": "bears"})
print(answer)