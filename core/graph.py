from langgraph.graph import StateGraph, END
from agents.retriever import retrieve
from agents.reasoner import reason, direct_answer
from agents.router import route
from typing import TypedDict

class AgentState(TypedDict):
    question: str
    context: list
    sources: list
    answer: str
    chat_history: list
    route: str
    pdf_indexed: bool

def decide_route(state: dict) -> str:
    return state.get("route", "direct")

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", route)
    graph.add_node("retriever", retrieve)
    graph.add_node("reasoner", reason)
    graph.add_node("direct_answer", direct_answer)

    graph.add_conditional_edges(
        "router",
        decide_route,
        {
            "search": "retriever",
            "direct": "direct_answer"
        }
    )

    graph.add_edge("retriever", "reasoner")
    graph.add_edge("reasoner", END)
    graph.add_edge("direct_answer", END)

    graph.set_entry_point("router")

    return graph.compile()

agent = build_graph()

def run_agent(question: str, chat_history: list = [], pdf_indexed: bool = False) -> dict:
    result = agent.invoke({
        "question": question,
        "context": [],
        "sources": [],
        "answer": "",
        "chat_history": chat_history,
        "route": "",
        "pdf_indexed": pdf_indexed
    })
    return result