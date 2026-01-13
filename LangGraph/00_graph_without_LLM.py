from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class LoanAppState(TypedDict):
    income:float
    age: int
    eligible: bool
    max_loan: float

def check_eligibility(state: LoanAppState) -> LoanAppState:
    income = state["income"]
    age = state["age"]
    eligible = False
    max_loan = 0.0

    if income > 50000 and age >= 21:
        eligible = True
        max_loan = income * 2.5
    
    state["eligible"] = eligible
    state["max_loan"] = max_loan

    return state

graph = StateGraph(LoanAppState)

graph.add_node('check_eligibility', check_eligibility)

graph.add_edge(START,'check_eligibility')
graph.add_edge('check_eligibility', END)

workflow = graph.compile()

initial_state = {
    "income": 5000,
    "age": 30
}

final_state = workflow.invoke(initial_state)

# print(final_state)
print(f"Eligible: {final_state['eligible']} \nMax Loan: {final_state['max_loan']}")

png = workflow.get_graph().draw_mermaid_png()
with open('LangGraph/loan_llm_workflow.png', 'wb') as f:
    f.write(png)

