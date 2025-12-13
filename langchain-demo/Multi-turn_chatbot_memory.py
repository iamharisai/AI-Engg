from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory


from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You're an assistant who's good at explaining things in single line answers."),
                MessagesPlaceholder("history"), "{input}"])

model = ChatOpenAI() # default 'model_name': 'gpt-3.5-turbo-0125'

parser = StrOutputParser()

chain = prompt | model | parser

session_id = "Hari-session-001"
store = {}

def get_by_session_id(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_by_session_id,
    input_messages_key="input",
    history_messages_key="history",
)

while True:
    user_text = input("You: ")
    if user_text.lower() in ["exit", "quit", "bye"]:
        break
    response = chain_with_history.invoke({"input": user_text},
                                         config ={"configurable": {"session_id": session_id}})
    print("AI: " + response)


#  Testing Output:
# You: What is AI
# AI: Artificial Intelligence is the simulation of human intelligence processes by machines, typically computer systems.
# You: What is LLM
# AI: Large Language Model, a type of artificial intelligence model capable of processing and generating human-like language.
# You: are they both connected? say yes or no
# AI: Yes.
# You: how they connected?
# AI: LLMs use AI technology to analyze and generate human-like language, making them a subset of artificial intelligence.
# You: bye