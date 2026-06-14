from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

os.environ['LANGSMITH_PROJECT'] = 'hari_2'
load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model1 = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.9)
model2 = ChatOpenAI(model='gpt-4o-mini', temperature=0.9)

parser = StrOutputParser()

chain = prompt1 | model1 | parser | prompt2 | model2 | parser

config = {
    'run_name': 'ai_penetration_report',
    'tags': ['demo', 'sequential_chain'],
    'metadata': {'topic': 'AI Penetration in India'}
}
result = chain.invoke({'topic': 'AI Penetration in India'}, config=config)

print(result)
