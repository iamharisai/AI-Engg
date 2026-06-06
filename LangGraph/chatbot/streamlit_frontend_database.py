import streamlit as st
from langgraph_backend_database import chatbot, llm, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid

# ***************************** Utility functions ****************************************
def generate_thread_id():
    return str(uuid.uuid4())

def reset_thread():
    st.session_state["thread_id"] = generate_thread_id()
    add_thread(st.session_state["thread_id"])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads'].keys():
        st.session_state['chat_threads'][thread_id] = None

def load_thread(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values
    return state.get("messages", [])

def name_thread(thread_id):
    if st.session_state['chat_threads'][thread_id] is not None:
        return
    messages = chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values.get("messages", [])
    if not messages:
        return
    instruction = HumanMessage(content="Reply with ONLY a 1-4 word title for this conversation. No quotes, no preamble, no trailing punctuation.")
    name = llm.invoke(messages + [instruction]).content.strip().strip('"').strip("'")
    st.session_state['chat_threads'][thread_id] = name

# ***************************** Session setup ****************************************
if 'thread_id' not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = {key: None for key in retrieve_all_threads()}

add_thread(st.session_state["thread_id"])

CONFIG = {'configurable': {'thread_id': st.session_state["thread_id"]}}
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
                temp_history.append({'role': 'user', 'content': message.content})
            elif isinstance(message, AIMessage):
                temp_history.append({'role': 'assistant', 'content': message.content})
        st.session_state['message_history'] = temp_history

# ***************************** Main conversation thread UI ****************************************

# loading the conversation history
for message in st.session_state['message_history'] :
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # first add the message to message_history
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, _ in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= CONFIG,
                stream_mode= 'messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    name_thread(st.session_state["thread_id"])