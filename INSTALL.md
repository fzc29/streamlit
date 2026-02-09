# Installation Instructions

## Quick Install

Run this command in your terminal:

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install streamlit python-dotenv PyPDF2 langchain-core langchain langchain-community langchain-text-splitters langchain-openai langchain-google-genai langchain-anthropic faiss-cpu google-generativeai anthropic pandas numpy scikit-learn sentence-transformers rank-bm25
```

## Verify Installation

After installation, verify the imports work:

```bash
python -c "import streamlit; from dotenv import load_dotenv; from PyPDF2 import PdfReader; from langchain_core.documents import Document; print('All imports successful!')"
```

## Note on Import Names

- `python-dotenv` package provides the `dotenv` module (import as `from dotenv import load_dotenv`)
- `PyPDF2` package provides the `PyPDF2` module (import as `from PyPDF2 import PdfReader`)
- `langchain-core` package provides the `langchain_core` module (import as `from langchain_core.documents import Document`)

## Troubleshooting

If you get permission errors, try:
- Using a virtual environment: `python -m venv venv && source venv/bin/activate`
- Using `pip install --user` instead
- Using conda: `conda install -c conda-forge streamlit python-dotenv pypdf2`

