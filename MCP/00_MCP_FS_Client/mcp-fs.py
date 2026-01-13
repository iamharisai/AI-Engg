import asyncio
import platform, os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

prompt = "create a file named hello.txt with the content 'Hello, World!' "
# prompt = "Summarize what is there in Readme.md file "

MCP_FOLDER = os.getenv("MCP_FOLDER_PATH")

# npx is in node.js
def npx_command():
    return "npx" if platform.system() != "Windows" else "npx.cmd"

async def chat(query):
    client = MultiServerMCPClient({
        "filesystem": {
            "transport": "stdio",
            "command" : npx_command(),
            "args": ["-y", "@modelcontextprotocol/server-filesystem", MCP_FOLDER]
        }
    })

    tools = await client.get_tools()

    llm = ChatOpenAI(model="gpt-4o")
    llm_with_tools = llm.bind_tools(tools)

    messages = []

    messages.append(SystemMessage(content= f"You are an expert file system assistant. All file operations in {MCP_FOLDER}"))
    messages.append(HumanMessage(content=query))
    
    while True:
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)

        if not ai_msg.tool_calls:
            return ai_msg.content
        
        for tc in ai_msg.tool_calls:
            tool_name = tc["name"]
            tool_args = tc["args"]
            tool_fn = next(tool for tool in tools if tool.name == tool_name)

            tool_result = await tool_fn.ainvoke(tool_args)
            messages.append(ToolMessage(content=str(tool_result), tool_call_id=tc["id"]))

response = asyncio.run(chat(prompt))
print(response)