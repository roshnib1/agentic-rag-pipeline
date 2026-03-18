import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Embedding model (free, runs locally)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Groq model
LLM_MODEL = "llama-3.3-70b-versatile"

# Chunking settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# FAISS index path
FAISS_INDEX_PATH = "vectorstore/faiss_index"

# RAG settings
TOP_K_RESULTS = 5