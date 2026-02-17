## Computer Requirements for Set up 

- Python 3.8 or higher
- API keys for:
  - Google Gemini (for embeddings)
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
   CLAUDE_MODEL=claude-3-5-sonnet-20241022
   CLAUDE_MAX_OUTPUT_TOKENS=2048
   CLAUDE_TEMPERATURE=0.0
   AGENT_CONTEXT_K=30
   ```
   
## Initial Setup

Before running the app, you need to build the vector indices from your existing documents:

1. **Organize your documents:**
   - Place PDF newsletters in an `october/` folder (or create folders like `newsletters/`, `context/`, `pnl/`)
   - The app expects PDF files in these folders

2. **Build the vector indices (optional - run once):**
   ```bash
   python rag.py
   ```
   
   This will process PDFs in the `october/` folder and create FAISS indices.

## Running the Application

1. **Start the Streamlit app:**
   ```bash
   streamlit run app2.py
   ```

2. **Open your browser:**
   The app will automatically open at `http://localhost:8501`

## Usage

### Querying Portfolio Data

1. Enter your query in the text area (or use the default prompt)
2. Click "🚀 Generate Newsletter"
3. Wait for the multi-agent system to analyze the data
4. View the generated newsletter and source documents

### Uploading Documents

1. Click "Browse files" in the sidebar
2. Select a PDF file
3. Choose which vector store to add it to:
   - `october`: For newsletter documents
   - `newsletters`: For newsletter examples
   - `context`: For market context documents
   - `pnl`: For P&L data
4. Click "➕ Add Document"
5. The document will be processed and added to the selected vector store

## Project Structure

```
streamlit/
├── app2.py              # Main Streamlit application
├── query_rag.py         # RAG query interface
├── multiagent.py        # Multi-agent orchestration system
├── rag.py              # Document processing and vector store management
├── embed.py            # Hybrid search and reranking utilities
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .env               # Environment variables (create this)
└── october/           # PDF documents folder
```

## How It Works

1. **Document Processing**: PDFs are read, chunked, and embedded using Google Gemini embeddings
2. **Vector Storage**: Documents are stored in FAISS vector databases for fast similarity search
3. **Query Processing**: When you submit a query:
   - **Market Context Agent**: Analyzes macro market drivers
   - **Portfolio Performance Agent**: Identifies top contributors/detractors
   - **Risk Analyst Agent**: Performs scenario analysis
   - **Newsletter Writer Agent**: Synthesizes everything into a newsletter
4. **Hybrid Search**: Combines dense (FAISS) and sparse (BM25) retrieval for better results
5. **Reranking**: Uses cross-encoder models to rerank results by relevance

## Troubleshooting

### Common Issues

1. **"FAISS index not found" error:**
   - Run `python rag.py` to build the initial indices
   - Make sure you have PDF files in the `october/` folder

2. **"API key not found" error:**
   - Check that your `.env` file exists and contains the required keys
   - Verify the keys are correct and have proper permissions

3. **Import errors:**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check that you're using the correct Python version (3.8+)

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

- **Test RAG processing:**
  ```bash
  python rag.py
  ```

- **Test multi-agent system:**
  ```bash
  python multiagent.py
  ```

### Adding New Features

- Modify `app2.py` for UI changes
- Modify `multiagent.py` for agent logic
- Modify `rag.py` for document processing
- Modify `embed.py` for search/retrieval improvements

## License

This project is for demonstration purposes.

## Support

For issues or questions, please check:
1. The troubleshooting section above
2. API provider documentation (Gemini, Claude)
3. Streamlit documentation: https://docs.streamlit.io/
