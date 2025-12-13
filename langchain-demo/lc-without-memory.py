from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI() # default 'model_name': 'gpt-3.5-turbo-0125'
# prompt = ChatPromptTemplate.from_template("you are a helpful assistant.")
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

# you can implement your own memory mechanism if needed

# method 0: In-memory variable to store the conversation (List/Array)
# method 1: Append the conversation to the prompt each time (not efficient for long conversations)
# method 2: Langchain's built-in memory modules (e.g., ConversationBufferMemory, ConversationSummaryMemory, etc.)
# method 3: Store the conversation externally (e.g., in a database) and retrieve relevant parts as needed
# method 4: Vector database - Use embeddings to find similar past conversations and include them in the prompt
# method 5: Combination of the above methods based on the use case and requirements