from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from core.config import GROQ_API_KEY, LLM_MODEL

def reason(state: dict) -> dict:
    question = state["question"]
    context = state["context"]
    sources = state["sources"]

    if not context:
        return {**state, "answer": "No relevant documents found. Please upload PDFs first."}

    context_str = ""
    for i, (chunk, source) in enumerate(zip(context, sources)):
        context_str += f"\n[Source {i+1}: {source}]\n{chunk}\n"

    prompt = PromptTemplate.from_template("""
You are an intelligent research assistant. Answer the question based ONLY on the provided context.
If the answer is not in the context, say "I could not find this in the uploaded documents."

Always mention which document(s) your answer comes from.

Context:
{context}

Question: {question}

Answer:
""")

    llm = ChatGroq(
        model=LLM_MODEL,
        groq_api_key=GROQ_API_KEY,
        temperature=0.2
    )

    chain = prompt | llm
    response = chain.invoke({
        "context": context_str,
        "question": question
    })

    return {**state, "answer": response.content}


def direct_answer(state: dict) -> dict:
    question = state["question"]

    prompt = PromptTemplate.from_template("""
You are a helpful assistant. Answer this general question conversationally.

Question: {question}

Answer:
""")

    llm = ChatGroq(
        model=LLM_MODEL,
        groq_api_key=GROQ_API_KEY,
        temperature=0.5
    )

    chain = prompt | llm
    response = chain.invoke({"question": question})

    return {**state, "answer": response.content, "sources": []}