# AI Engineering

Notes and code examples exploring AI engineering concepts including LLM integrations, agents, RAG, and more.

## Project Structure

```
AI-Engg/
├── 101/                    # Getting started with LLM SDKs
│   ├── openai-sdk.py       # OpenAI SDK basics
│   └── gemini-sdk.py       # Google Gemini SDK basics
│
├── Old-school-requests/    # Direct API calls using requests library
│   └── openai-req.py       # Raw HTTP requests to OpenAI API
│
├── langchain-demo/         # LangChain fundamentals
│   ├── lc-basicQA.py       # Basic Q&A with prompt templates
│   ├── lc-without-memory.py
│   └── Multi-turn_chatbot_memory.py  # Chatbot with conversation memory
│
├── Tool-calling/           # Function/tool calling with LLMs
│   ├── ddg_tool.py         # DuckDuckGo search tool
│   └── custom_tools/       # Building custom tools
│       ├── datetime_tool-V0.py
│       ├── datetime_tool-V1.py
│       └── multi_tool.py
│
├── Agents/                 # LLM Agents
│   ├── 00_react_agent.py   # ReAct agent with tools
│   └── 01_agent.py
│
├── RAG/                    # Retrieval Augmented Generation
│   └── product_recommendation.py  # Product recommendations with ChromaDB
│
├── LangGraph/              # Graph-based LLM workflows
│   ├── 00_graph_without_LLM.py
│   ├── 01_joke_simulator.py
│   ├── 02_parallel_workflow.py
│   └── 03_batsman.py
│
└── MCP/                    # Model Context Protocol
    ├── 00_MCP_FS_Client/   # File system MCP client
    └── 01_MCP_Server/      # Custom MCP server & client
```

## Topics Covered

- **LLM SDK Basics** - Direct usage of OpenAI and Gemini SDKs
- **LangChain** - Chains, prompts, output parsers, and memory
- **Tool Calling** - Integrating external tools and functions with LLMs
- **Agents** - ReAct pattern agents that reason and act
- **RAG** - Vector stores (ChromaDB), embeddings, and retrieval chains
- **LangGraph** - State machines and parallel workflows for complex LLM apps
- **MCP** - Model Context Protocol for connecting AI to external systems

## Setup

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd AI-Engg

# Install dependencies using uv
uv sync
```

### Environment Variables

Create a `.env` file with your API keys:

```
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
```

## Running Examples

```bash
# Run any example with uv
uv run python 101/openai-sdk.py
uv run python langchain-demo/lc-basicQA.py
uv run python RAG/product_recommendation.py
```

## Dependencies

Key libraries used in this project:

- `openai` - OpenAI Python SDK
- `google-genai` - Google Gemini SDK
- `langchain` / `langchain-openai` - LangChain framework
- `langgraph` - Graph-based LLM workflows
- `langchain-chroma` - ChromaDB vector store integration
- `fastmcp` / `langchain-mcp-adapters` - Model Context Protocol
- `ddgs` - DuckDuckGo search
