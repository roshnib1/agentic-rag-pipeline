# Agentic Document Research Assistant

An end-to-end agentic RAG pipeline that lets you upload multiple PDFs and ask complex questions across all of them using LangGraph, FAISS, and Groq LLM.

## Features
- Upload multiple PDFs and index them with FAISS
- Agentic pipeline using LangGraph (retriever + reasoner nodes)
- Free embeddings using HuggingFace (all-MiniLM-L6-v2)
- Free LLM using Groq (Llama 3.3 70B)
- Source tracking — shows which document the answer came from
- Session memory for follow-up questions
- Clean Streamlit UI

## Tech Stack
- LangGraph — agentic pipeline
- LangChain — orchestration
- FAISS — vector store
- HuggingFace Sentence Transformers — embeddings
- Groq (Llama 3.3 70B) — LLM
- Streamlit — UI
- RAGAS — evaluation (coming soon)

## Setup

1. Clone the repo
   git clone https://github.com/roshnib1/agentic-rag-pipeline.git
   cd agentic-rag-pipeline

2. Create virtual environment
   python -m venv venv
   venv\Scripts\Activate

3. Install dependencies
   pip install -r requirements.txt

4. Add your API keys to .env
   GROQ_API_KEY=your_groq_key_here
   GOOGLE_API_KEY=your_google_key_here

5. Run the app
   python main.py

## Project Structure
   agents/         — retriever and reasoner nodes
   core/           — config, PDF loader, LangGraph pipeline
   vectorstore/    — FAISS indexing and retrieval
   evaluation/     — RAGAS evaluation
   ui/             — Streamlit app

## Usage
1. Upload one or more PDFs in the sidebar
2. Click Index Documents
3. Ask any question in the chat
4. The agent retrieves relevant chunks and generates a grounded answer
5. Sources are shown for every answer