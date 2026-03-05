import streamlit as st
import os
import csv
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
# File Loaders
# ============================================================

def load_pdf(path: Path) -> list[Document]:
    loader = PyPDFLoader(str(path))
    return loader.load()

def load_md(path: Path) -> list[Document]:
    text = path.read_text(encoding="utf-8")
    return [Document(page_content=text, metadata={"source": path.name})]

def load_csv(path: Path) -> list[Document]:
    docs = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            content = "\n".join(f"{k}: {v}" for k, v in row.items())
            docs.append(Document(page_content=content, metadata={"source": path.name, "row": i}))
    return docs

def load_file(path: Path) -> list[Document]:
    ext = path.suffix.lower()
    if ext == ".pdf":
        return load_pdf(path)
    elif ext == ".md":
        return load_md(path)
    elif ext == ".csv":
        return load_csv(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

# ============================================================
# UI
# ============================================================

st.title("📂 Upload & Index Documents")

uploaded_files = st.file_uploader("Upload Doc (pdf, markdown, CSV)", 
                                 type=["pdf", "md", "csv"], 
                                 accept_multiple_files=True
                                 )

store_type = st.selectbox(
    "Select Knowledge Base",
    ["context", "pnl", "newsletter", "weekly_market_data"]
)

if uploaded_files and st.button("Index Document"):

    BASE_DIR = Path(__file__).resolve().parent
    index_path = BASE_DIR / f"{store_type}_faiss_index"

    all_chunks = []
    errors = []

    with st.spinner("Processing and embedding document..."):

        for uploaded_file in uploaded_files: 
            temp_path = BASE_DIR / uploaded_file.name
            try:
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                docs = load_file(temp_path) 

                # Chunk
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                )
                chunks = splitter.split_documents(docs)
                all_chunks.extend(chunks)
                st.write(f"{uploaded_file.name}` — {len(chunks)} chunks")

            except Exception as e:
                errors.append(f"{uploaded_file.name}: {str(e)}")
                st.warning(f"Error processing {uploaded_file.name}: {str(e)}") 

            finally:
                if temp_path.exists():
                    os.remove(temp_path)

        if all_chunks:
            if index_path.exists():
                vectorstore = FAISS.load_local(
                    str(index_path),
                    embeddings=embedding,
                    allow_dangerous_deserialization=True,
                )
                vectorstore.add_documents(all_chunks)
                st.info("Updated existing index.")
            else:
                vectorstore = FAISS.from_documents(chunks, embedding)
                st.info("Created new index.")

            vectorstore.save_local(str(index_path))

    if all_chunks:
        st.success(f"Document indexed successfully! {len(all_chunks)} total chunks indexed into `{store_type}`.")
    if errors:
        st.error(f"Failed to process: {', '.join(errors)}")
