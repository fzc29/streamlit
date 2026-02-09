# Quick Start Guide

Since you already have the FAISS index (`october_faiss_index`), follow these steps:

## Step 1: Install Core Packages (Skip FAISS for now)

```bash
pip install -r requirements-minimal.txt
```

This installs everything except FAISS.

## Step 2: Install FAISS

You have 3 options (try in order):

### Option A: Use Conda (Easiest - Pre-built binaries)
```bash
conda install -c conda-forge faiss-cpu -y
```

### Option B: Install cmake first, then FAISS
```bash
# Install cmake
brew install cmake  # macOS
# OR
conda install -c conda-forge cmake -y

# Then install FAISS
pip install faiss-cpu
```

### Option C: Use the install script
```bash
./install-faiss.sh
```

## Step 3: Verify Installation

```bash
python -c "import streamlit; from dotenv import load_dotenv; from PyPDF2 import PdfReader; from langchain_core.documents import Document; import faiss; print('✅ All imports successful!')"
```

## Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
CLAUDE_API_KEY=your_claude_api_key_here
EMBEDDING_PROVIDER=gemini
```

## Step 5: Run the App

```bash
streamlit run app2.py
```

## Troubleshooting FAISS Installation

If FAISS still fails to install:

1. **Try upgrading pip first:**
   ```bash
   pip install --upgrade pip
   pip install faiss-cpu
   ```

2. **Use conda instead of pip:**
   ```bash
   conda install -c conda-forge faiss-cpu
   ```

3. **Install from wheel (if available for your platform):**
   ```bash
   pip install faiss-cpu --no-build-isolation
   ```

4. **Check Python version:** FAISS requires Python 3.8-3.11
   ```bash
   python --version
   ```

## Note About Missing Indices

The app expects these FAISS indices:
- `october_faiss_index` ✅ (you have this)
- `newsletters_faiss_index` (optional - only needed for newsletter examples)
- `context_faiss_index` (optional - only needed for market context)
- `pnl_faiss_index` (optional - only needed for P&L data)

If you only have `october_faiss_index`, the app will work but some features may be limited. The multi-agent system will try to load all indices, but will gracefully handle missing ones if we update the code.

