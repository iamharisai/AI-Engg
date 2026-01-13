from datetime import datetime, timezone
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import tool,DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage,ToolMessage,AIMessage,SystemMessage
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

load_dotenv()

# custom tool
@tool("get_current_datetime")
def get_current_datetime():
    """Returns the current date and time as a string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

# in-built tool
search_tool = DuckDuckGoSearchRun()

model = ChatOpenAI(model_name="gpt-4o")
tools = [get_current_datetime, search_tool]
model_with_tools = model.bind_tools(tools)

prompt = PromptTemplate.from_template("""
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
                                      """)

agent = create_react_agent(model, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def chat(query: str) -> str:
    result = agent_executor.invoke({"input": query})
    return result["output"]

query = "What is time now in place which visited by Messi in December 2025"
response = chat(query)
print(response)