from fastmcp import FastMCP
from datetime import datetime, timezone
from langchain_community.tools import DuckDuckGoSearchRun

mcp = FastMCP("MyMCPServer")

search_tool = DuckDuckGoSearchRun()

@mcp.tool()
def get_current_datetime() -> str:
    """get the current date and time in UTC."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool()
def web_search(query: str) -> str:
    """Search the web using duckduckgo"""
    return search_tool.run(query)

mcp.run(transport="sse", host="localhost", port= 8000)
