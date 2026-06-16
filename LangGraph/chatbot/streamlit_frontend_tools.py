import streamlit as st
from langgraph_backend_tools import (
    chatbot,
    llm,
    create_thread,
    set_thread_title,
    list_threads,
)
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import uuid
import os

os.environ["LANGSMITH_PROJECT"] = "Chatbot_tools"

# ***************************** Utility functions ****************************************
def extract_text(content):
    """Normalize message.content to a plain string across providers.

    OpenAI -> str; Anthropic -> list of blocks ({type:'text'|'tool_use', ...}).
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "".join(parts)
    return ""

def generate_thread_id():
    return str(uuid.uuid4())

def reset_thread():
    st.session_state["thread_id"] = generate_thread_id()
    st.session_state['message_history'] = []

def persist_thread(thread_id):
    """Insert the thread row on first successful Q+A. Idempotent."""
    if thread_id not in st.session_state['chat_threads']:
        create_thread(thread_id)
        st.session_state['chat_threads'][thread_id] = None

def load_thread(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values
    return state.get("messages", [])

def name_thread(thread_id):
    if st.session_state['chat_threads'].get(thread_id) is not None:
        return
    messages = chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values.get("messages", [])
    if not messages:
        return
    instruction = HumanMessage(content="Reply with ONLY a 1-4 word title for this conversation. No quotes, no preamble, no trailing punctuation.")
    name = llm.invoke(messages + [instruction]).content.strip().strip('"').strip("'")
    st.session_state['chat_threads'][thread_id] = name
    set_thread_title(thread_id, name)

# ***************************** Session setup ****************************************
if 'thread_id' not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = dict(list_threads())

CONFIG = { 'configurable': {'thread_id': st.session_state["thread_id"]},
            # "metadata": {"thread_name": st.session_state['chat_threads'][st.session_state["thread_id"]]},
            "run_name": "chat_turn",}
# ***************************** Sidebar session ****************************************

st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_thread()

st.sidebar.header("Conversation Threads")
for thread_id in reversed(list(st.session_state['chat_threads'].keys())):
    label = st.session_state['chat_threads'][thread_id] or "Untitled"
    if st.sidebar.button(label, key=thread_id):
        st.session_state["thread_id"] = thread_id
        messages = load_thread(thread_id)

        temp_history = []
        for message in messages:
            if isinstance(message, HumanMessage):
                temp_history.append({'role': 'user', 'content': extract_text(message.content)})
            elif isinstance(message, AIMessage):
                text = extract_text(message.content)
                if text:  # skip pure tool_use turns with no visible text
                    temp_history.append({'role': 'assistant', 'content': text})
        st.session_state['message_history'] = temp_history

# ***************************** Main conversation thread UI ****************************************

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    # Assistant streaming block
    with st.chat_message("assistant"):
        # Use a mutable holder so the generator can set/modify it
        status_holder = {"box": None}

        def ai_only_stream():
            # Tracks whether a tool just ran, so we can break the previous
            # AI segment from the next one (otherwise "...:" + "## Header"
            # concatenate and markdown stops rendering the header).
            pending_break = {"v": False}

            for message_chunk, _metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                # Lazily create & update the SAME status container when any tool runs
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}` …", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🔧 Using `{tool_name}` …",
                            state="running",
                            expanded=True,
                        )
                    pending_break["v"] = True
                    continue

                # Stream ONLY assistant tokens. Content shape differs by provider:
                # OpenAI -> str; Anthropic -> list of blocks like
                # [{"type": "text", "text": "..."}, {"type": "tool_use", ...}].
                if isinstance(message_chunk, AIMessage):
                    content = message_chunk.content
                    texts = []
                    if isinstance(content, str):
                        if content:
                            texts.append(content)
                    elif isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "text":
                                t = block.get("text", "")
                                if t:
                                    texts.append(t)
                            elif isinstance(block, str) and block:
                                texts.append(block)

                    for t in texts:
                        if pending_break["v"]:
                            yield "\n\n"
                            pending_break["v"] = False
                        yield t

        ai_message = st.write_stream(ai_only_stream())

        # Finalize only if a tool was actually used
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool finished", state="complete", expanded=False
            )

    # Save assistant message
    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )
    persist_thread(st.session_state["thread_id"])
    name_thread(st.session_state["thread_id"])
