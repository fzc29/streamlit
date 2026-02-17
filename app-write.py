import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_core.documents import Document

from trash.rag import chunk_text, store_vector

load_dotenv()

st.set_page_config(page_title="RAG Admin", page_icon="📂", layout="centered")

# ---------------------------
# Password Protection
# ---------------------------

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

password = st.text_input("Admin Password", type="password")

if password != ADMIN_PASSWORD:
    st.stop()

# ---------------------------
# UI
# ---------------------------

st.title("📂 Upload & Index Documents")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

store_type = st.selectbox(
    "Select Knowledge Base",
    ["context", "pnl", "newsletters"]
)

if uploaded_file and st.button("Index Document"):

    with st.spinner("Reading and processing document..."):

        # Extract text
        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        if not text.strip():
            st.error("No text extracted from PDF.")
            st.stop()

        doc = Document(
            page_content=text,
            metadata={"source": uploaded_file.name}
        )

        chunks = chunk_text([doc])

        base_dir = os.path.dirname(__file__)
        index_path = os.path.join(base_dir, f"{store_type}_faiss_index")

        store_vector(index_path, chunks)

    st.success("Document indexed successfully.")
