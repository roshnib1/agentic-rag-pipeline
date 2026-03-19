from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from vectorstore.indexer import load_index
from agents.reasoner import reason
from agents.retriever import retrieve
from core.config import GROQ_API_KEY, LLM_MODEL
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from core.config import EMBEDDING_MODEL
import pandas as pd

def run_evaluation(test_questions: list) -> pd.DataFrame:
    questions = []
    answers = []
    contexts = []

    print("Running evaluation...")

    for question in test_questions:
        # Run the retriever
        state = {
            "question": question,
            "context": [],
            "sources": [],
            "answer": "",
            "chat_history": [],
            "route": ""
        }

        state = retrieve(state)
        state = reason(state)

        questions.append(question)
        answers.append(state["answer"])
        contexts.append(state["context"])

    # Build RAGAS dataset
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
    }

    dataset = Dataset.from_dict(data)

    # Use Groq as LLM for evaluation
    llm = ChatGroq(
        model=LLM_MODEL,
        groq_api_key=GROQ_API_KEY,
        temperature=0
    )

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # Run RAGAS evaluation
    results = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy],
        llm=llm,
        embeddings=embeddings
    )
    df = results.to_pandas()
    
    # Print actual columns so we can see what RAGAS returns
    print("Available columns:", df.columns.tolist())
    print(df)
    
    return df