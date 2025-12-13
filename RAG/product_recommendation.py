from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# Load products data
Loader = TextLoader("RAG/products.txt", encoding="utf8")
docs = Loader.load()
# print(docs[0].page_content)

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(docs)
# print(len(splits)) # 6 chunks

# Create vector store from chunks and retriever
vectordb = Chroma.from_documents(splits, embedding=OpenAIEmbeddings(), persist_directory="RAG/chroma_db")

retriver = vectordb.as_retriever(search_kwargs={"k":3})


# Define prompt template
template = """You are a product recommendation assistant, which recommend simillar products. 
                Use the following product information to answer the user's query.
                {context}
                Product_name: {product_name}
                Answer like product: <product_name> by brand, and mention short reason in one sentense and addd 2-3 bullet points for why recommended
                If you don't know the answer, just say “No strong matches found.”. Do not make up an answer.
                """

prompt = PromptTemplate.from_template(template)

model = ChatOpenAI(model_name="gpt-4o")

parser = StrOutputParser()

# create a chain
chain = ({"context": retriver, "product_name": RunnablePassthrough() } 
        | prompt
        | model
        | parser)

def recommend_products(product_name: str, k = 5) -> str:
    return chain.invoke(product_name)

# response = chain.invoke("Can you recommend any products for vacation with kids?")
# print("Product Recommendation Response: ")
# print(response)

print (recommend_products(product_name="chappal",k=2))


# output
# Product_name: Flip-Flops by Havaianas

# Reason: Chappals, similar to flip-flops, are commonly known for their lightweight design and comfortable wear, making them an ideal casual footwear choice.

# - Rubber sole provides flexibility and durability.
# - The comfortable strap makes them easy to wear for long periods.
# - Lightweight design perfect for casual and everyday use.
# (.venv) harisai.marisa@MAC-H2LWT644XR AI-Engg % 