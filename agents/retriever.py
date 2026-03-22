import cmd

from vectorstore.indexer import load_index
from core.config import TOP_K_RESULTS

def retrieve(state: dict) -> dict:
    question = state["question"]
    vectorstore = load_index()

    if vectorstore is None:
        return {**state, "context": [], "sources": []}

    docs = vectorstore.similarity_search(question, k=TOP_K_RESULTS)

    context = [doc.page_content for doc in docs]
    sources = [doc.metadata.get("source", "Unknown") for doc in docs]

    print(f"Retrieved {len(docs)} chunks for: '{question}'")

    return {**state, "context": context, "sources": sources}