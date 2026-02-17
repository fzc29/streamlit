## Computer Requirements for Set up 

- Python 3.11 preferred (choose through python Interpreter during project setup) 
- API keys for:
  - Google Gemini/OpenAI (for embeddings)
  - Anthropic Claude (for LLM queries)

## Installation Process

1. **Clone or navigate to the project directory:**

2. **Create a virtual environment**
   ```python -m ve_name venv```
   - To activate venv use command: 
      a. MAC: ```source ve_name/bin/activate```
      b. Windows: ``` ve_name/Scripts/activate```

3. **Install dependencies:**
   ```pip install -r requirements.txt``` 
   if the above doesn't work, try installing with ```python -m pip install __```

4. **Set up environment variables:**
   
   Create a `.env` file in the project root with the following variables:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   CLAUDE_API_KEY=your_claude_api_key_here
   EMBEDDING_PROVIDER=gemini
   CLAUDE_MODEL=claude-3-haiku-20240307
   CLAUDE_MAX_OUTPUT_TOKENS=2048
   CLAUDE_TEMPERATURE=0.0
   AGENT_CONTEXT_K=30
   ```
   
## Initial Setup

Before running the app, you need to build the vector indices from your existing documents:

1. **Organize your documents:**
   - The app expects PDF files in these folders (newsletters, pnl, context) 
   - future updates may allow other options of categories 

2. **Build the vector indices (run once in the beginning to create [categor]_faiss_index):**
   ```python buildindex.py```
   This will process PDFs in the all of the folders in /data and create FAISS indices.

## Testing the Application

1. **Deploy locally through:**
   ```streamlit run [interface py file]```

2. **Open your browser:**
   The app will automatically open at `http://localhost:8501` (unless otherwise specified) 

## Usage

### Querying Portfolio Data

1. Enter your query in the text area (or use the default prompt)
2. Click "Generate Response"
3. Wait for the multi-agent system to analyze the data
4. View the generated newsletter and source documents

### Uploading Documents

1. Login in as Admin
2. Select a PDF file (upload)
3. Choose which vector store to add it to:
   - `newsletters`: For newsletter examples
   - `context`: For market context documents
   - `pnl`: For P&L data
4. Click "➕ Add Document"
5. The document will be processed and added to the selected vector store in backend 
               (logic needs to be improved here for better organization, scalability, etc)

## Project Structure

```
streamlit/
├── app-query.py         # Main Streamlit application for querying for responses
├── app-write.py         # Main Streamlit application for adding to FAISS vector DB
├── multiagent.py        # Multi-agent orchestration system
├── buildindex.py        # Document processing and vector store management
├── embed.py             # Hybrid search and reranking utilities
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── .env                 # Environment variables (create this)
└── data/                # PDF documents folder 
```

## How It Works

## Troubleshooting Common Issues

1. **"FAISS index not found" error:**
   - Run `python rag.py` to build the initial indices
   - Make sure you have PDF files in the `october/` folder

2. **"API key not found" error:**
   - Check that your `.env` file exists and contains the required keys
   - Verify the keys are correct and have proper permissions

3. **Import errors:**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check that you're using the correct Python version

4. **File upload not working:**
   - Ensure the target folder exists (e.g., `october/`, `newsletters/`, etc.)
   - Check file permissions
   - Verify the PDF is not corrupted

5. **OMP Error**
   - add environment variables to terminal 
      * echo 'export KMP_DUPLICATE_LIB_OK=TRUE' >> ~/.zshrc
      * echo 'export OMP_NUM_THREADS=1' >> ~/.zshrc
      * source ~/.zshrc
      - then reopen terminal to save these changes 
   - OR ```brew install libomp``` (fixes behavior on Apple Silicon), make sure to restart terminal
   - Usually doesn't occur on windows 

### Environment Variables

If you encounter issues, verify your `.env` file has all required variables:
- `GEMINI_API_KEY` (required)
- `CLAUDE_API_KEY` (required)
- `EMBEDDING_PROVIDER` (optional, defaults to "gemini")
- `CLAUDE_MODEL` (optional, defaults to "claude-3-5-sonnet-20241022")

## Development

### Testing Individual Components

- **Test Backend Alone multi-agent system:**
   - focus on multiagent.py for main process -> ```python multiagent.py```
   - embedding techniques stored in embed.py 

- **Testing both interfaces simultaneously**
   - ```streamlit run app-query.py --server.port 8501```
   - ```streamlit run app-write.py --server.port 8502```


## Other Resources

1. First check troubleshooting section above
2. API provider documentation (Gemini, Claude)
3. Streamlit documentation: https://docs.streamlit.io/

