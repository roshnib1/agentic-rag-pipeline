from core.config import GROQ_API_KEY

def route(state: dict) -> dict:
    question = state["question"].strip().lower()

    # Rule-based greetings — always direct
    greetings = ["hello", "hi", "hey", "how are you", "thanks",
                 "thank you", "bye", "good morning", "good night",
                 "who are you", "what is your name", "okay", "ok"]

    for word in greetings:
        if word in question:
            print("Router decision: direct (greeting)")
            return {**state, "route": "direct"}

    # Check if PDF was indexed in this session
    pdf_indexed = state.get("pdf_indexed", False)

    if pdf_indexed:
        print("Router decision: search (PDF indexed)")
        return {**state, "route": "search"}

    print("Router decision: direct (no PDF in session)")
    return {**state, "route": "direct"}