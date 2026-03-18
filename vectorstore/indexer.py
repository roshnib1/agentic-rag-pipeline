from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from core.config import EMBEDDING_MODEL, FAISS_INDEX_PATH
import os

def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def create_index(docs: list):
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(FAISS_INDEX_PATH)
    print(f"FAISS index saved — {len(docs)} chunks indexed")
    return vectorstore

def load_index():
    if not os.path.exists(FAISS_INDEX_PATH):
        return None
    embeddings = get_embeddings()
    return FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )