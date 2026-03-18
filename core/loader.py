from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from core.config import CHUNK_SIZE, CHUNK_OVERLAP
import os

def load_pdfs(uploaded_files: list, save_dir: str = "uploaded_docs") -> list:
    os.makedirs(save_dir, exist_ok=True)
    all_docs = []

    for uploaded_file in uploaded_files:
        file_path = os.path.join(save_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        loader = PyPDFLoader(file_path)
        pages = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = splitter.split_documents(pages)

        for chunk in chunks:
            chunk.metadata["source"] = uploaded_file.name

        all_docs.extend(chunks)
        print(f"Loaded {uploaded_file.name} — {len(chunks)} chunks")

    return all_docs