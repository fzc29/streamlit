"""
Query RAG interface for app2.py
Provides a simplified interface to the multi-agent system
"""
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from multiagent import build_agent_system

# Load environment variables
load_dotenv()

# Initialize the orchestrator agent system
_orchestrator = None

def get_orchestrator():
    """Lazy initialization of the orchestrator."""
    global _orchestrator
    if _orchestrator is None:
        try:
            _orchestrator = build_agent_system()
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize agent system: {str(e)}\n"
                "Make sure you have:\n"
                "1. Set GEMINI_API_KEY and CLAUDE_API_KEY in .env\n"
                "2. Built the FAISS indices by running: python rag.py"
            ) from e
    return _orchestrator

def multi_stage_query(query: str):
    """
    Execute a multi-stage query using the orchestrator agent system.
    
    Args:
        query: The user's query/prompt
        
    Returns:
        tuple: (answer_object, docs_list)
        - answer_object: Object with .content attribute containing the newsletter
        - docs_list: List of Document objects used in the query
    """
    orchestrator = get_orchestrator()
    
    # Run the query sequentially (more reliable for demo)
    result = orchestrator.run_sequential(query)
    
    # Extract the newsletter content
    newsletter_content = result["newsletter"]["newsletter"]
    
    # Collect all source documents from all agents
    all_docs = []
    
    # Collect sources from market context
    if "sources" in result.get("market_context", {}):
        for source in result["market_context"]["sources"]:
            all_docs.append(Document(
                page_content="",
                metadata={"source": source, "agent": "MarketContextAgent"}
            ))
    
    # Collect sources from portfolio performance
    if "sources" in result.get("portfolio_performance", {}):
        for source in result["portfolio_performance"]["sources"]:
            all_docs.append(Document(
                page_content="",
                metadata={"source": source, "agent": "PortfolioPerformanceAgent"}
            ))
    
    # Collect sources from newsletter writer
    if "sources" in result.get("newsletter", {}):
        for source in result["newsletter"]["sources"]:
            all_docs.append(Document(
                page_content="",
                metadata={"source": source, "agent": "NewsletterWriterAgent"}
            ))
    
    # Create a simple answer object with content attribute
    class Answer:
        def __init__(self, content):
            self.content = content
    
    answer = Answer(newsletter_content)
    
    return answer, all_docs

def load_vector(index_name: str):
    """
    Load a vector store by name.
    Note: This is a placeholder for compatibility with app2.py
    The actual vector stores are managed internally by the agents.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(base_dir, f"{index_name}_faiss_index")
    
    if not os.path.exists(index_path):
        return None
    
    # Return a placeholder object for compatibility
    class VectorStore:
        def __init__(self, path):
            self.path = path
    
    return VectorStore(index_path)

# Placeholder stores for compatibility (not actually used in the new system)
newsletter_store = None
context_store = None
pnl_store = None

