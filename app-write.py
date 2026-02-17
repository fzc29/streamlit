import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings

load_dotenv()

st.set_page_config(
    page_title="RAG Admin",
    page_icon="📂",
    layout="centered"
)

# ============================================================
# Password Protection
# ============================================================

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

password = st.text_input("Admin Password", type="password")

if password != ADMIN_PASSWORD:
    st.stop()

# ============================================================
# Embedding Setup (Cached)
# ============================================================

@st.cache_resource
def get_embedding():
    provider = os.getenv("EMBEDDING_PROVIDER", "gemini").lower()

    if provider == "openai":
        return OpenAIEmbeddings(
            model="text-embedding-3-large",
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    elif provider == "gemini":
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY"),
        )

    else:
        raise ValueError("Unsupported embedding provider.")

embedding = get_embedding()

# ============================================================
# UI
# ============================================================

st.title("📂 Upload & Index Documents")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

store_type = st.selectbox(
    "Select Knowledge Base",
    ["context", "pnl", "newsletter"]
)

if uploaded_file and st.button("Index Document"):

    with st.spinner("Processing and embedding document..."):

        # Save temp file
        BASE_DIR = Path(__file__).resolve().parent
        temp_path = BASE_DIR / uploaded_file.name

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Load PDF
        loader = PyPDFLoader(str(temp_path))
        docs = loader.load()

        # Chunk
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        chunks = splitter.split_documents(docs)

        # Determine index path
        index_path = BASE_DIR / f"{store_type}_faiss_index"

        if index_path.exists():
            vectorstore = FAISS.load_local(
                str(index_path),
                embeddings=embedding,
                allow_dangerous_deserialization=True,
            )
            vectorstore.add_documents(chunks)
            st.info("Updated existing index.")
        else:
            vectorstore = FAISS.from_documents(chunks, embedding)
            st.info("Created new index.")

        vectorstore.save_local(str(index_path))

        # Cleanup temp file (not storing raw PDF, just the vector embeddings)
        os.remove(temp_path)

    st.success("Document indexed successfully.")
