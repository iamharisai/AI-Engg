# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About This Repo

Personal learning notes and code examples from a structured AI engineering course (Telusko). Each folder is a self-contained module covering a specific concept, progressing from raw API calls up to agentic systems.

## Commands

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies
uv sync

# Run any script
uv run python <module>/<script>.py

# Examples
uv run python 101/openai-sdk.py
uv run python LangGraph/01_joke_simulator.py
uv run python MCP/01_MCP_Server/01_mcp_server.py
```

There are no tests or linting configured.

## Environment Variables

A `.env` file is required at the project root. Scripts load it via `python-dotenv`:

```
OPENAI_API_KEY=...
GEMINI_API_KEY=...          # used by 101/gemini-sdk.py
MCP_FOLDER_PATH=...         # absolute path used by the MCP client (e.g. MCP/00_MCP_FS_Client/)
```

## Architecture & Learning Path

Modules build on each other in this order:

| Module | What it teaches |
|---|---|
| `101/` | Bare SDK calls — OpenAI and Gemini, no frameworks |
| `Old-school-requests/` | Raw HTTP to OpenAI REST API |
| `langchain-demo/` | LangChain chains, prompt templates, memory |
| `Tool-calling/` | Binding tools to an LLM; custom `@tool` decorators |
| `Agents/` | ReAct-pattern agents that loop over tool calls autonomously |
| `RAG/` | ChromaDB vector store + OpenAI embeddings + retrieval chains |
| `LangGraph/` | State machine workflows over typed state dicts |
| `MCP/` | Model Context Protocol: server exposes tools, client discovers and calls them |

## Key Patterns

**LangGraph** — graphs are built with `StateGraph(MyTypedDict)`, nodes are plain functions that receive and return the state dict, edges (including conditional branches) connect them. Call `graph.compile()` then `.invoke(initial_state)`.

**MCP** — two-part setup:
1. `MCP/01_MCP_Server/01_mcp_server.py` defines tools with `@mcp.tool()` via `FastMCP` and runs an SSE server on `localhost:8000`.
2. `MCP/01_MCP_Server/02_mcp_client.py` (and `MCP/00_MCP_FS_Client/`) connects via `MultiServerMCPClient`, fetches tools, binds them to a `ChatOpenAI` model, and runs a manual tool-call loop with `LangChain` message types.

**RAG** — `RAG/product_recommendation.py` ingests text into ChromaDB with OpenAI embeddings, then uses a retrieval chain to answer questions grounded in that data. The `chroma_db/` directory is persisted locally.
