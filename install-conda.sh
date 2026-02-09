#!/bin/bash
# Install packages using conda (recommended for Anaconda users)

echo "Installing packages via conda..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating venv..."
    source venv/bin/activate
fi

# Install via conda (preferred for Anaconda)
conda install -c conda-forge -y \
    streamlit \
    python-dotenv \
    pypdf2 \
    pandas \
    numpy \
    scikit-learn

# Install langchain packages via pip (conda doesn't have all langchain packages)
echo "Installing LangChain packages via pip..."
pip install --user \
    langchain-core \
    langchain \
    langchain-community \
    langchain-text-splitters \
    langchain-google-genai \
    langchain-anthropic \
    google-generativeai \
    anthropic \
    sentence-transformers \
    rank-bm25

# Install FAISS
echo "Installing FAISS..."
conda install -c conda-forge faiss-cpu -y

echo "✅ Installation complete!"
echo ""
echo "To verify, run:"
echo "  python -c \"import streamlit; print('Streamlit OK')\""

