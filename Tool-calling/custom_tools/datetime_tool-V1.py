from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import tool
from langchain_core.messages import HumanMessage,ToolMessage,AIMessage,SystemMessage

load_dotenv()

@tool("get_current_datetime")
def get_current_datetime():
    """Returns the current date and time as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

model = ChatOpenAI(model_name="gpt-4o")

model_with_tools = model.bind_tools([get_current_datetime])

messages = []
query  = "What is the current date?"
messages.append(HumanMessage(content=query))

ai_msg = model_with_tools.invoke(messages)
messages.append(ai_msg)

# check if there is tool_call needed
if ai_msg.tool_calls[0]["name"] == "get_current_datetime":
    tool_msg = get_current_datetime.invoke({})
    messages.append(ToolMessage(content=tool_msg, tool_call_id=ai_msg.tool_calls[0]["id"]))
    ai_msg = model_with_tools.invoke(messages)
    messages.append(ai_msg)

# The last message will be AI message
print(messages[-1].content)
# The current date is December 29, 2025.

