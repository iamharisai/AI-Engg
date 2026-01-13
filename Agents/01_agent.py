from datetime import datetime, timezone
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import tool,DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage,ToolMessage,AIMessage,SystemMessage
from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate

load_dotenv()

# custom tool
@tool("get_current_datetime")
def get_current_datetime():
    """Returns the current date and time as a string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

# in-built tool
search_tool = DuckDuckGoSearchRun()

model = ChatOpenAI(model_name="gpt-5")
tools = [get_current_datetime, search_tool]
model_with_tools = model.bind_tools(tools)

prompt = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
                                      """

# agent = create_agent(model=model, tools= tools, system_prompt=prompt)

agent = create_agent(model=model, tools= tools)

def chat(query: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result

query = "What is time now in country which visited by Messi in December 2025"
response = chat(query)
print(response["messages"][-1].content)