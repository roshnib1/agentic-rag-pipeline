from langgraph.graph import StateGraph, END
from agents.retriever import retrieve
from agents.reasoner import reason
from typing import TypedDict

# Define the state schema
class AgentState(TypedDict):
    question: str
    context: list
    sources: list
    answer: str
    chat_history: list

def build_graph():
    # Create the graph
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("retriever", retrieve)
    graph.add_node("reasoner", reason)

    # Add edges — retriever always goes to reasoner
    graph.add_edge("retriever", "reasoner")
    graph.add_edge("reasoner", END)

    # Entry point
    graph.set_entry_point("retriever")

    return graph.compile()

# Single instance
agent = build_graph()

def run_agent(question: str, chat_history: list = []) -> dict:
    result = agent.invoke({
        "question": question,
        "context": [],
        "sources": [],
        "answer": "",
        "chat_history": chat_history
    })
    return result