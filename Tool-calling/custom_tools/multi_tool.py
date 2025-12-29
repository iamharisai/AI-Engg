from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import tool,DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage,ToolMessage,AIMessage,SystemMessage

load_dotenv()

# custom tool
@tool("get_current_datetime")
def get_current_datetime():
    """Returns the current date and time as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# in-built tool
search_tool = DuckDuckGoSearchRun()

model = ChatOpenAI(model_name="gpt-4o")
tools = [get_current_datetime, search_tool]
model_with_tools = model.bind_tools(tools)

def chat(query: str) -> str:
    messages = []
    messages.append(HumanMessage(content=query))

    while True:
        ai_msg = model_with_tools.invoke(messages)
        messages.append(ai_msg)
        if not ai_msg.tool_calls:
            return ai_msg.content

        for tc in ai_msg.tool_calls:
            tool_name = tc["name"]
            tool_args = tc["args"]
            tool_fn = next(t for t in tools if t.name == tool_name)
            tool_msg = tool_fn.invoke(tool_args)
            messages.append(ToolMessage(content=tool_msg, tool_call_id=tc["id"]))

query = "What is time in place which visited by Messi in December 2025"
response = chat(query)
print(response)
# Lionel Messi is set to visit India in December 2025 as part of the "GOAT Tour." The tour begins on December 12, 2025, in Kolkata and includes stops in Hyderabad, Mumbai, and Delhi from December 13-15, 2025.
# As for the current time at your location as of now (2025), it is 14:17 on December 29, 2025.