from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
import sqlite3, os, requests

load_dotenv()

# 1. LLM
llm = ChatAnthropic(model="claude-haiku-4-5", temperature=0, max_tokens=4096)

# 2. Tools
search_tool = DuckDuckGoSearchResults(region="us-en")

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}

@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    r = requests.get(url)
    return r.json()

tools = [search_tool, get_stock_price, calculator]
llm_with_tools = llm.bind_tools(tools)

# 3. State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# 4. Nodes
def chat_node(state: ChatState):
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

# 5. Checkpointer
conn = sqlite3.connect('chatbot_history.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

# App-owned table for thread metadata (titles). Lives next to the checkpointer's tables.
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS threads (
        thread_id  TEXT PRIMARY KEY,
        title      TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """
)
conn.commit()

# 6. Graph
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge('tools', 'chat_node')


chatbot = graph.compile(checkpointer=checkpointer)

# 7. Helpers
def create_thread(thread_id: str) -> None:
    conn.execute("INSERT OR IGNORE INTO threads (thread_id) VALUES (?)", (thread_id,))
    conn.commit()

def set_thread_title(thread_id: str, title: str) -> None:
    conn.execute(
        "UPDATE threads SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE thread_id = ?",
        (title, thread_id),
    )
    conn.commit()

def list_threads() -> dict[str, str | None]:
    rows = conn.execute(
        "SELECT thread_id, title FROM threads ORDER BY created_at ASC"
    ).fetchall()
    return {thread_id: title for thread_id, title in rows}
