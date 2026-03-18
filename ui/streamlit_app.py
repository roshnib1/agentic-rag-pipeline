import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.loader import load_pdfs
from vectorstore.indexer import create_index, load_index
from core.graph import run_agent

st.set_page_config(
    page_title="Doc Research Agent",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Agentic Document Research Assistant")
st.caption("Upload multiple PDFs and ask complex questions across all of them")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "indexed" not in st.session_state:
    st.session_state.indexed = False

# Sidebar — PDF upload
with st.sidebar:
    st.header("📄 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("Index Documents", type="primary"):
            with st.spinner("Loading and indexing PDFs..."):
                docs = load_pdfs(uploaded_files)
                create_index(docs)
                st.session_state.indexed = True
                st.success(f"Indexed {len(docs)} chunks from {len(uploaded_files)} PDF(s)!")

    st.divider()

    if st.session_state.indexed:
        st.success("✅ Documents ready")
    else:
        st.warning("⚠️ No documents indexed yet")

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Main chat area
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📚 Sources"):
                for source in set(message["sources"]):
                    st.write(f"• {source}")

# Chat input
question = st.chat_input("Ask a question about your documents...")

if question:
    if not st.session_state.indexed:
        st.error("Please upload and index documents first!")
    else:
        # Show user message
        with st.chat_message("user"):
            st.write(question)

        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = run_agent(question, st.session_state.chat_history)
                answer = result["answer"]
                sources = list(set(result["sources"]))

            st.write(answer)

            if sources:
                with st.expander("📚 Sources"):
                    for source in sources:
                        st.write(f"• {source}")

        # Save to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })