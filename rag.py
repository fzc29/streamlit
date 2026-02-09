import os
import glob
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
# from langchain_community.vectorstores import FAISS
# from langchain_community.text_splitter import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain.schema.document import Document
from langchain_core.documents import Document

import google.generativeai as genai
import pandas as pd
from embed import *

# Load API key from .env
load_dotenv()

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "gemini")  # "openai" or "gemini"

if EMBEDDING_PROVIDER.lower() == "openai":
    from langchain.embeddings.openai import OpenAIEmbeddings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    embedding = OpenAIEmbeddings(
        model="text-embedding-3-large",
        openai_api_key=OPENAI_API_KEY
    )
elif EMBEDDING_PROVIDER.lower() == "gemini":
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    import google.generativeai as genai
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GEMINI_API_KEY
    )
elif EMBEDDING_PROVIDER.lower() == "claude":
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    import google.generativeai as genai
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GEMINI_API_KEY
    )
else:
    raise ValueError(f"Unknown embedding provider: {EMBEDDING_PROVIDER}")

# API_KEY = os.getenv("API_KEY")
# genai.configure(api_key=API_KEY)

# locating files 
base_dir = os.path.dirname(os.path.abspath(__file__))
# print("base_dir: ", base_dir)

newsletter_folder = os.path.join(base_dir, "newsletters")
# print("source_dir: ", newsletter_folder)
num_news_pdfs = len(glob.glob(os.path.join(newsletter_folder, "*.pdf")))
# print(f"→ Found {num_news_pdfs} PDFs in news_dir")

context_folder = os.path.join(base_dir, "context")  
# print("target_dir: ", context_folder)
num_news_pdfs = len(glob.glob(os.path.join(context_folder, "*.pdf")))
# print(f"→ Found {num_news_pdfs} PDFs in context_dir")

pnl_folder = os.path.join(base_dir, "pnl")  

october = os.path.join(base_dir, "october") 


# # Gemini Embeddings
# embedding = GoogleGenerativeAIEmbeddings(
#     model="models/embedding-001",
#     google_api_key=API_KEY
# )

def read_pdf_from_folder(folder):
    all_text = []
    pdf_files = glob.glob(os.path.join(folder, "*.pdf"))
    print(f"Found {len(pdf_files)} PDFs in {folder}")

    for filepath in pdf_files:
        # print(f"Processing: {filepath}")
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
            else:
                print("No text extracted from page")

        if text.strip():
            print("text added")
            all_text.append(Document(page_content=text, metadata={"source": filepath}))
        else:
            print(f"WARNING: No text found in {filepath}")

    return all_text 

# Load output from our PNL automation 
def load_markdown_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    return Document(page_content=content, metadata={"source": filepath})

def load_csv_file(filepath):
    df = pd.read_csv(filepath)
    content = df.to_markdown(index=False)
    return Document(page_content=content, metadata={"source": filepath})

def chunk_text(docs, chunk_size=1000, chunk_overlap=400):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
    return text_splitter.split_documents(docs)


# input path should be the index_path: index_path = os.path.join(base_dir, "faiss_index")
# weekly_letter_index = os.path.join(base_dir, "weekly_letter_index", "faiss_index")
def store_vector(path, docs):

    if os.path.exists(path):
        vectorstore = FAISS.load_local(
            path,
            embeddings=embedding,
            allow_dangerous_deserialization=True
        )
        vectorstore.add_documents(docs)
    else:
        vectorstore = FAISS.from_documents(docs, embedding)

    # print("location of FAISS index: ", path)
    vectorstore.save_local(path)
    print("Vector store sucessfully updated and saved to 'faiss_index/'")

def process_folder(folder_name):
    docs = read_pdf_from_folder(folder_name)
    chunks =  chunk_text(docs)

    index_path = os.path.join(base_dir, f"{folder_name}_faiss_index")
    store_vector(index_path, chunks)


def process_pnl(folder_path):
    md_files = glob.glob(os.path.join(folder_path, "*.md"))
    pnl_docs = []
    for pnl in md_files:
        pnl_docs.append(load_markdown_file(pnl))

    pnl_chunks = chunk_text(pnl_docs)
    pnl_index = os.path.join(base_dir, "pnl_faiss_index")
    store_vector(pnl_index, pnl_chunks)


# ========== Run on all target folders ==========
folders_to_process = [october]

for folder in folders_to_process:
    process_folder(folder)

# process_pnl(pnl_folder)