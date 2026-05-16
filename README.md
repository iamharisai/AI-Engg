# AI Engineering

This repository is my personal learning path for AI engineering. I initially started with the AI Engineering course by Telusko. During the breaks, I followed LangGraph's playlist from the CampusX YouTube playlist.

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

## Learning Plan

### Phase 1 — Foundations ✅ Complete

| Topic | Folder | What's built |
|---|---|---|
| LLM SDK Basics | `101/` | Direct OpenAI & Gemini API calls |
| Raw HTTP | `Old-school-requests/` | `requests` lib against OpenAI REST |
| LangChain | `langchain-demo/` | Chains, prompt templates, output parsers |
| Memory | `langchain-demo/` | Stateful multi-turn chatbot with `RunnableWithMessageHistory` |
| Tool Calling | `Tool-calling/` | DuckDuckGo + custom `@tool` decorators, manual tool loop |
| Agents | `Agents/` | ReAct pattern with `create_react_agent` |
| RAG | `RAG/` | ChromaDB + OpenAI embeddings + retrieval chain |

### Phase 2 — LangGraph 🔄 In Progress

Following the [CampusX LangGraph playlist](https://github.com/campusx-official/langgraph-tutorials):

| # | Topic | File | Status |
|---|---|---|---|
| 1 | Graph basics, no LLM (BMI/Loan workflow) | `LangGraph/00_graph_without_LLM.py` | ✅ |
| 2 | Simple LLM workflow | `LangGraph/01_joke_simulator.py` | ✅ |
| 3 | Prompt chaining | `LangGraph/04_prompt_chaining.ipynb` | ✅ |
| 4 | Parallel workflow | `LangGraph/02_parallel_workflow.py`, `03_batsman.py` | ✅ |
| 5 | UPSC essay workflow | `LangGraph/05_essay_evaluator.ipynb` | ✅ |
| 6 | Conditional edges / routing | `LangGraph/06_review_handler.ipynb` | ✅ |
| 7 | Review reply workflow | `LangGraph/06_review_handler.ipynb` | ✅ |
| 8 | X post generator | `LangGraph/07_X_post_generator.ipynb` | ✅ |
| 9 | Basic chatbot in LangGraph | — | ❌ |
| 10 | Persistence (checkpointers, thread IDs) | — | ❌ |
| 11 | Tools in LangGraph | — | ❌ |
| 12 | MCP | `MCP/` | ✅ Done separately |
| 13 | RAG in LangGraph | `RAG/` | ✅ Done separately |
| 14 | Human-in-the-Loop (HITL) | — | ❌ |
| 15 | Subgraphs + shared state | — | ❌ |

**Remaining order:** 9 (chatbot) → 10 (persistence) → 11 (tools) → 14 (HITL) → 15 (subgraphs)

### Phase 3 — Fine-tuning 🔜 Up Next

Started with `Fine-tuning/huggingfacedemo.ipynb` (HuggingFace Hub, dataset loading, streaming).
Next: LoRA/QLoRA fine-tuning on an open model, pushing adapters to Hub, inference with fine-tuned model.

---

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
