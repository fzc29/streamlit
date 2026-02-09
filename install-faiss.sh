#!/bin/bash
# Script to install FAISS with workarounds for cmake issues

echo "Installing FAISS-CPU..."

# Option 1: Try installing via conda (if available)
if command -v conda &> /dev/null; then
    echo "Found conda, trying conda install..."
    conda install -c conda-forge faiss-cpu -y
    if [ $? -eq 0 ]; then
        echo "✅ FAISS installed via conda!"
        exit 0
    fi
fi

# Option 2: Install cmake first, then faiss-cpu
if ! command -v cmake &> /dev/null; then
    echo "cmake not found. Installing cmake..."
    
    # Try homebrew (macOS)
    if command -v brew &> /dev/null; then
        brew install cmake
    # Try conda
    elif command -v conda &> /dev/null; then
        conda install -c conda-forge cmake -y
    else
        echo "⚠️  Please install cmake manually:"
        echo "   macOS: brew install cmake"
        echo "   Or: conda install -c conda-forge cmake"
        exit 1
    fi
fi

# Option 3: Try pip install with pre-built wheel
echo "Trying pip install faiss-cpu..."
pip install faiss-cpu --no-build-isolation

if [ $? -ne 0 ]; then
    echo "⚠️  FAISS installation failed. Trying alternative..."
    pip install faiss-cpu --no-cache-dir
fi

echo "✅ Installation complete!"

