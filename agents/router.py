from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from core.config import GROQ_API_KEY

def route(state: dict) -> dict:
    question = state["question"]

    prompt = PromptTemplate.from_template("""
You are a routing agent. Decide if the question needs searching documents or can be answered directly.

Reply with ONLY one word:
- "search" if the question is about specific information, facts, research, or content from documents
- "direct" if the question is a greeting, general knowledge, or casual conversation

Question: {question}

Decision:
""")

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=GROQ_API_KEY,
        temperature=0
    )

    chain = prompt | llm
    decision = chain.invoke({"question": question}).content.strip().lower()

    print(f"Router decision: {decision}")

    # Default to search if unclear
    if "direct" in decision:
        return {**state, "route": "direct"}
    return {**state, "route": "search"}