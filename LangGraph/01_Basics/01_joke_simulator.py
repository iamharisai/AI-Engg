from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-4o')
model1 = ChatOpenAI(model='gpt-5')

class JokeState(TypedDict):
    topic: str
    joke: str
    rating: int

def smart_comedian(state: JokeState) -> JokeState:
    prompt = f"Tell me a funny joke about {state['topic']} in single line."
    joke = model.invoke(prompt)
    state['joke'] = joke
    return state

def rate_joke(state: JokeState) -> JokeState:
    prompt = f"Rate this joke: {state['joke']}, which is about topic: {state['topic']} from 1 to 5 based on their creativity and humor. Penalize them heavily for lack of creativity and humor, Just reply with a rating number"
    rating = model1.invoke(prompt)

    state['rating'] = rating
    return state


graph = StateGraph(JokeState)

graph.add_node('smart_comedian', smart_comedian)
graph.add_node('rate_joke', rate_joke)

graph.add_edge(START, 'smart_comedian')
graph.add_edge('smart_comedian', 'rate_joke')
graph.add_edge('rate_joke', END)

workflow = graph.compile()

initial_state = {
    "topic": "software developing"
}

final_state = workflow.invoke(initial_state)

# print(final_state)
print(f"Joke: {final_state['joke'].content} \nRating: {final_state['rating'].content}")

png = workflow.get_graph().draw_mermaid_png()
with open('LangGraph/llm_workflow.png', 'wb') as f:
    f.write(png)