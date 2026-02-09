# Fixing pip Permission Errors

You're getting permission errors with pip. Since you're using **Anaconda**, use **conda** instead:

## ✅ Solution: Use Conda

### Option 1: Install via conda (Recommended)

```bash
# Activate your venv if you have one
source venv/bin/activate

# Install core packages via conda
conda install -c conda-forge -y streamlit python-dotenv pypdf2 pandas numpy scikit-learn faiss-cpu

# Install LangChain packages via pip (with --user flag to avoid permissions)
pip install --user langchain-core langchain langchain-community langchain-text-splitters langchain-google-genai langchain-anthropic google-generativeai anthropic sentence-transformers rank-bm25
```

### Option 2: Use the install script

```bash
./install-conda.sh
```

### Option 3: Install in your venv specifically

```bash
# Make sure you're in venv
source venv/bin/activate

# Use python -m pip instead of pip directly
python -m pip install streamlit python-dotenv PyPDF2

# Then install LangChain packages
python -m pip install langchain-core langchain langchain-community langchain-text-splitters langchain-google-genai langchain-anthropic google-generativeai anthropic sentence-transformers rank-bm25

# Install FAISS via conda
conda install -c conda-forge faiss-cpu -y
```

## Quick Test

After installation, verify:

```bash
python -c "import streamlit; print('✅ Streamlit works!')"
```

## Why This Happens

The permission error occurs because pip is trying to modify system-level SSL certificates. Using conda or `pip install --user` avoids this issue.

