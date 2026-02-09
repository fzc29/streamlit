# app2.py
import streamlit as st
import os
from dotenv import load_dotenv

# Import your existing RAG functions
from query_rag import multi_stage_query
from rag import chunk_text, store_vector

# Load environment
load_dotenv()

# Page config
st.set_page_config(
    page_title="Portfolio Analysis RAG",
    page_icon="💼",
    layout="wide"
)

# Title
st.title("💼 Portfolio Analysis Assistant")
st.markdown("Monthly newsletter generation powered by RAG")

# Sidebar for settings and file upload
with st.sidebar:
    st.header("📊 System Status")
    st.success("✅ RAG System Loaded")
    st.info("📁 Vector Stores Active")
    
    st.divider()
    
    st.header("📤 Upload Documents")
    uploaded_file = st.file_uploader(
        "Upload PDF document",
        type=['pdf'],
        help="Upload a PDF file to add to the knowledge base"
    )
    
    if uploaded_file is not None:
        # Store selection
        store_type = st.selectbox(
            "Add to which store?",
            ["october", "newsletters", "context", "pnl"],
            help="Select which vector store to add this document to"
        )
        
        if st.button("➕ Add Document", type="primary"):
            with st.spinner("Processing and indexing document..."):
                try:
                    # Save uploaded file temporarily
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    target_folder = os.path.join(base_dir, store_type)
                    
                    # Create folder if it doesn't exist
                    os.makedirs(target_folder, exist_ok=True)
                    
                    # Save file
                    file_path = os.path.join(target_folder, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Process and index the document
                    from rag import embedding
                    from PyPDF2 import PdfReader
                    from langchain_core.documents import Document
                    
                    # Read PDF directly
                    reader = PdfReader(file_path)
                    text = ""
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text
                    
                    if text.strip():
                        # Create document
                        doc = Document(page_content=text, metadata={"source": file_path})
                        
                        # Chunk the document
                        chunks = chunk_text([doc])
                        
                        # Store in vector index
                        index_path = os.path.join(base_dir, f"{store_type}_faiss_index")
                        store_vector(index_path, chunks)
                        
                        st.success(f"✅ Document '{uploaded_file.name}' added to {store_type} store!")
                        
                        # Clear the file uploader by rerunning
                        st.rerun()
                    else:
                        st.error("Failed to extract text from PDF. The file may be empty or corrupted.")
                        
                except Exception as e:
                    st.error(f"❌ Error processing file: {str(e)}")
                    st.exception(e)
    
    st.divider()
    
    st.markdown("""
    **Available Stores:**
    - October (Newsletters)
    - Market Context  
    - P&L Data
    """)

# Main chat interface
st.subheader("Generate Monthly Newsletter")

# Pre-defined prompt (you can make this editable)
default_prompt = """
You are an AI portfolio analyst for a discretionary global macro hedge fund.
Analyze October 2025 monthly performance data and produce a monthly newsletter.

Tasks:
1. Explain the core macro thesis underlying the portfolio
2. Identify top contributors and detractors to P&L
3. Link portfolio outcomes to macro drivers from the RAG context
4. Provide scenario analysis (base/upside/downside)
"""

# Prompt input (optional - can just use button if you want single-click demo)
user_prompt = st.text_area(
    "Query/Prompt:",
    value=default_prompt,
    height=200
)

# Generate button
if st.button("🚀 Generate Newsletter", type="primary"):
    with st.spinner("Analyzing portfolio data and generating newsletter..."):
        try:
            # Call your existing function
            answer, docs = multi_stage_query(user_prompt)
            
            # Display result
            st.success("✅ Newsletter Generated!")
            
            # Main output
            st.markdown("### 📰 Generated Newsletter")
            st.markdown(answer.content)
            
            # Sources (collapsible)
            with st.expander("🔍 View Retrieved Sources"):
                st.markdown("**Documents used for this analysis:**")
                for idx, doc in enumerate(docs[:10], start=1):  # Show top 10
                    source = doc.metadata.get('source', 'unknown')
                    # Clean up the path for display
                    source_name = os.path.basename(source)
                    st.markdown(f"{idx}. `{source_name}`")
                
                if len(docs) > 10:
                    st.caption(f"...and {len(docs) - 10} more sources")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.exception(e)

# Footer
st.divider()
st.caption("Powered by LangChain + FAISS + Claude/Gemini")

# Note: Make sure you have the required environment variables set in .env:
# - GEMINI_API_KEY (for embeddings)
# - CLAUDE_API_KEY (for Claude model)
# - EMBEDDING_PROVIDER (optional, defaults to "gemini")