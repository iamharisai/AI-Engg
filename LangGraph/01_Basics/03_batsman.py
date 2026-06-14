# batsman_langgraph.py

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. Define the state that flows through the graph
class BatsmanState(TypedDict, total=False):
    runs: int
    balls: int
    fours: int
    sixes: int
    sr: float               # strike rate
    bpb: float              # balls per boundary
    boundary_percent: float
    summary: str


# 2. Define node functions

def calculate_strike_rate(state: BatsmanState) -> BatsmanState:
    runs = state["runs"]
    balls = state["balls"]
    # Avoid division by zero
    sr = (runs / balls * 100) if balls > 0 else 0.0
    return {"sr": sr}


def calculate_balls_per_boundary(state: BatsmanState) -> BatsmanState:
    balls = state["balls"]
    fours = state["fours"]
    sixes = state["sixes"]
    total_boundaries = fours + sixes
    # Balls per boundary = total balls / total boundaries
    bpb = (balls / total_boundaries) if total_boundaries > 0 else float("inf")
    return {"bpb": bpb}


def calculate_boundary_percent(state: BatsmanState) -> BatsmanState:
    runs = state["runs"]
    fours = state["fours"]
    sixes = state["sixes"]
    boundary_runs = fours * 4 + sixes * 6
    boundary_percent = (boundary_runs / runs * 100) if runs > 0 else 0.0
    return {"boundary_percent": boundary_percent}


def summary(state: BatsmanState) -> BatsmanState:
    sr = state.get("sr", 0.0)
    bpb = state.get("bpb", 0.0)
    boundary_percent = state.get("boundary_percent", 0.0)

    text = (
        f"Strike Rate: {sr:.2f}\n"
        f"Balls per boundary: {bpb:.2f}\n"
        f"Boundary percent: {boundary_percent:.2f}%"
    )
    return {"summary": text}


def build_workflow():
    # 3. Create the graph with the shared state type
    graph = StateGraph(BatsmanState)

    # 4. Add nodes
    graph.add_node("calculate_strike_rate", calculate_strike_rate)
    graph.add_node("calculate_balls_per_boundary", calculate_balls_per_boundary)
    graph.add_node("calculate_boundary_percent", calculate_boundary_percent)
    graph.add_node("summary", summary)

    # 5. Wire edges for a PARALLEL workflow:
    # START -> all three calculators in parallel -> summary -> END
    graph.add_edge(START, "calculate_strike_rate")
    graph.add_edge(START, "calculate_balls_per_boundary")
    graph.add_edge(START, "calculate_boundary_percent")

    # All three converge into summary
    graph.add_edge("calculate_strike_rate", "summary")
    graph.add_edge("calculate_balls_per_boundary", "summary")
    graph.add_edge("calculate_boundary_percent", "summary")

    graph.add_edge("summary", END)

    # 6. Compile the graph into an executable app
    app = graph.compile()
    return app


if __name__ == "__main__":
    workflow = build_workflow()

    # Example input state
    initial_state: BatsmanState = {
        "runs": 40,
        "balls": 20,
        "fours": 10,
        "sixes": 0,
    }

    final_state = workflow.invoke(initial_state)

    print("Final state:")
    for k, v in final_state.items():
        print(f"{k}: {v}")
