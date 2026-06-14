from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

load_dotenv()

llm = ChatOpenAI()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

# Checkpointer
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

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

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
