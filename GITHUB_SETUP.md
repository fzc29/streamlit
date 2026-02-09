# Uploading to GitHub - Step by Step Guide

## Step 1: Create a .gitignore (Already Done ✅)

The `.gitignore` file has been created to exclude:
- `.env` files (API keys - **NEVER commit these!**)
- `venv/` (virtual environment)
- FAISS indices (large binary files)
- Python cache files
- OS-specific files

## Step 2: Initialize Git (if not already done)

```bash
cd /Users/yuanxinchen/streamlit
git init
```

## Step 3: Add All Files

```bash
# Add all files (respecting .gitignore)
git add .

# Check what will be committed
git status
```

## Step 4: Create Initial Commit

```bash
git commit -m "Initial commit: Portfolio Analysis RAG System"
```

## Step 5: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Name it (e.g., `portfolio-rag-system`)
4. **Don't** initialize with README (you already have one)
5. Click **"Create repository"**

## Step 6: Connect and Push

GitHub will show you commands. Use these:

```bash
# Add the remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Important: Before Pushing

### ⚠️ Check for Sensitive Files

Make sure you **don't commit**:
- `.env` file (contains API keys)
- Any files with API keys or passwords

Verify:
```bash
git status
```

If `.env` shows up, it's not being ignored. Check `.gitignore` or remove it:
```bash
git rm --cached .env  # Remove from git but keep local file
```

### 📝 Update README

Make sure `README.md` doesn't contain:
- Actual API keys
- Personal information you don't want public

## Quick Commands Summary

```bash
# Initialize
git init

# Add files
git add .

# Commit
git commit -m "Initial commit"

# Connect to GitHub (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push
git push -u origin main
```

## What Gets Uploaded

✅ **Will be uploaded:**
- All Python files (`.py`)
- `requirements.txt` and `requirements-minimal.txt`
- `README.md` and other documentation
- PDF files in `october/` folder (unless you exclude them)

❌ **Will NOT be uploaded** (thanks to `.gitignore`):
- `.env` file (API keys)
- `venv/` folder
- FAISS indices (`*_faiss_index/`)
- Python cache files
- OS files (`.DS_Store`, etc.)

## After Uploading

1. **Add a `.env.example` file** (optional but recommended):
   ```bash
   # Create example env file
   cat > .env.example << EOF
   GEMINI_API_KEY=your_gemini_api_key_here
   CLAUDE_API_KEY=your_claude_api_key_here
   EMBEDDING_PROVIDER=gemini
   EOF
   ```

2. **Update README** with setup instructions

3. **Add a license** if you want (MIT, Apache, etc.)

## Troubleshooting

### "Permission denied" error
- Make sure you're authenticated with GitHub
- Use SSH instead: `git remote add origin git@github.com:USERNAME/REPO.git`

### "Large file" error
- FAISS indices might be too large
- Make sure `*_faiss_index/` is in `.gitignore`
- Use Git LFS for large files if needed

### Want to exclude PDFs too?
Uncomment this line in `.gitignore`:
```
# *.pdf
```

