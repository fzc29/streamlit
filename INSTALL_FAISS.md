# Installing FAISS-CPU (Workaround for cmake issues)

Since `faiss-cpu` requires `cmake` to build from source, here are the easiest solutions:

## ✅ Recommended: Use Conda

Conda has pre-built FAISS binaries, so no compilation needed:

```bash
conda install -c conda-forge faiss-cpu -y
```

## Alternative: Install cmake first

### macOS (using Homebrew):
```bash
brew install cmake
pip install faiss-cpu
```

### Using Conda for cmake:
```bash
conda install -c conda-forge cmake -y
pip install faiss-cpu
```

## Quick Test

After installation, verify:
```bash
python -c "import faiss; print('✅ FAISS installed successfully!')"
```

## If Still Failing

1. **Upgrade pip:**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install faiss-cpu
   ```

2. **Try without build isolation:**
   ```bash
   pip install faiss-cpu --no-build-isolation
   ```

3. **Check Python version:** FAISS works with Python 3.8-3.11
   ```bash
   python --version
   ```

4. **Use the install script:**
   ```bash
   ./install-faiss.sh
   ```

