#  Agentic RAG Research & Quiz Assistant
 
An intelligent document research assistant built with **LangGraph**, **FAISS**, and **Groq LLM**. Upload any PDF and either ask complex questions across all documents or auto-generate a quiz to test your understanding — powered by a multi-agent pipeline that makes decisions at runtime.
 
---
## ✨ Features
 
- **Multi-agent LangGraph pipeline** — router node intelligently decides whether to search documents or answer directly
- **Semantic search** — FAISS vector store with HuggingFace embeddings for fast, accurate retrieval
- **Multi-document support** — upload multiple PDFs and search across all of them simultaneously
- **Source tracking** — every answer shows exactly which document it came from
- **Quiz generation** — auto-generate MCQ and True/False questions at Easy, Medium, or Hard difficulty from any PDF
- **Interactive quiz mode** — answer questions one by one, get instant feedback and explanations, see final score with full review
- **RAGAS evaluation** — measure pipeline quality with faithfulness and answer relevancy metrics

---

## Stack
 
- LangGraph — agent pipeline with conditional routing
- LangChain — LLM orchestration
- FAISS — local vector store
- HuggingFace (all-MiniLM-L6-v2) — free local embeddings
- Groq (Llama 3.3 70B) — LLM
- RAGAS — evaluation
- Streamlit — UI
 
---

## Setup

1. Clone the repo
   git clone https://github.com/roshnib1/agentic-rag-pipeline.git
   cd agentic-rag-pipeline

2. Create virtual environment
   python -m venv venv
   venv\Scripts\Activate #Windows

3. Install dependencies
   pip install -r requirements.txt

4. Add your API keys to .env
   GROQ_API_KEY=your_groq_key_here
   GOOGLE_API_KEY=your_google_key_here

5. Run the app
   python main.py

## Project structure
 
```
├── agents/
│   ├── retriever.py       # searches FAISS
│   ├── reasoner.py        # generates answer
│   ├── router.py          # decides search vs direct
│   └── quiz_generator.py  # generates quiz from PDF
├── core/
│   ├── config.py
│   ├── loader.py          # PDF loading and chunking
│   └── graph.py           # LangGraph pipeline
├── vectorstore/
│   └── indexer.py
├── evaluation/
│   └── evaluator.py       # RAGAS evaluation
├── ui/
│   └── streamlit_app.py
└── main.py
```
Made by [Roshni Behera](https://github.com/roshnib1)