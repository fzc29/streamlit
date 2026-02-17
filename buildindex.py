import os
import glob
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.documents import Document
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    CSVLoader,
    TextLoader
)

# =========================
# Environment + Embeddings
# =========================

load_dotenv()

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "gemini").lower()

if EMBEDDING_PROVIDER == "openai":
    from langchain_openai import OpenAIEmbeddings

    embedding = OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

elif EMBEDDING_PROVIDER == "gemini":
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    embedding = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )

else:
    raise ValueError(f"Unsupported EMBEDDING_PROVIDER: {EMBEDDING_PROVIDER}")


# =========================
# Paths
# =========================

BASE_DIR = Path(__file__).resolve().parent

CONTEXT_DIR = BASE_DIR / "data" /"context"
NEWSLETTER_DIR = BASE_DIR / "data" / "newsletters"
PNL_DIR = BASE_DIR / "data" / "pnl"

CONTEXT_INDEX = BASE_DIR / "context_faiss_index"
NEWSLETTER_INDEX = BASE_DIR / "newsletter_faiss_index"
PNL_INDEX = BASE_DIR / "pnl_faiss_index"


# =========================
# Document Loading
# =========================

def load_documents(folder: Path):
    documents = []

    for file in folder.rglob("*"):
        if file.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file))
        elif file.suffix.lower() == ".md":
            loader = UnstructuredMarkdownLoader(str(file))
        elif file.suffix.lower() == ".csv":
            loader = CSVLoader(str(file))
        elif file.suffix.lower() == ".txt":
            loader = TextLoader(str(file))
        else:
            continue

        docs = loader.load()
        documents.extend(docs)

    return documents


# =========================
# Chunking
# =========================

def chunk_documents(docs, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(docs)


# =========================
# FAISS Storage
# =========================

def build_or_update_index(index_path: Path, docs):
    if index_path.exists():
        vectorstore = FAISS.load_local(
            str(index_path),
            embeddings=embedding,
            allow_dangerous_deserialization=True,
        )
        vectorstore.add_documents(docs)
        print(f"Updated existing index → {index_path.name}")
    else:
        vectorstore = FAISS.from_documents(docs, embedding)
        print(f"Created new index → {index_path.name}")

    vectorstore.save_local(str(index_path))


# =========================
# Processing Pipelines
# =========================

def process_folder(folder: Path, index_path: Path):
    if not folder.exists():
        print(f"Folder not found: {folder}")
        return

    print(f"\nProcessing folder: {folder.name}")
    docs = load_documents(folder)

    if not docs:
        print("No documents found.")
        return

    chunks = chunk_documents(docs)
    build_or_update_index(index_path, chunks)


# =========================
# Main Execution
# =========================

if __name__ == "__main__":
    process_folder(CONTEXT_DIR, CONTEXT_INDEX)
    process_folder(NEWSLETTER_DIR, NEWSLETTER_INDEX)
    process_folder(PNL_DIR, PNL_INDEX)

    print("\nAll FAISS indexes built successfully.")
