from rank_bm25 import BM25Okapi
import numpy as np
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

# ==================
# HYBRID RETRIEVAL
# ==================
def hybrid_search(query, faiss_store, docs, embedding_model, alpha=0.5, k=30):
    """Combines dense (FAISS) + sparse (BM25) retrieval."""
    # Dense retrieval
    faiss_results = faiss_store.vectorstore.similarity_search(query, k=k)
    dense_scores = np.linspace(1, 0, len(faiss_results))
    
    # Sparse retrieval
    tokenized_corpus = [d.page_content.split() for d in docs]
    bm25 = BM25Okapi(tokenized_corpus)
    sparse_scores = bm25.get_scores(query.split())
    top_sparse_idx = np.argsort(sparse_scores)[::-1][:k]
    sparse_results = [docs[i] for i in top_sparse_idx]
    
    # Merge scores
    combined = {}
    for i, d in enumerate(faiss_results):
        combined[d.page_content] = alpha * dense_scores[i]
    for i, d in enumerate(sparse_results):
        combined[d.page_content] = combined.get(d.page_content, 0) + (1 - alpha) * sparse_scores[top_sparse_idx[i]]
    
    # Sort merged results
    sorted_docs = sorted(combined.items(), key=lambda x: x[1], reverse=True)
    return [Document(page_content=t[0]) for t in sorted_docs[:k]]


# ====================
# RELEVANCE RERANKING
# ====================
cross_encoder = CrossEncoder("BAAI/bge-reranker-base")

def rerank(query, docs, k=30):
    """Re-ranks documents using cross-encoder."""
    pairs = [(query, d.page_content) for d in docs]
    scores = cross_encoder.predict(pairs)
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [d for d, _ in ranked[:k]]