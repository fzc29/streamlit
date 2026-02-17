"""
Hybrid Retrieval + Reranking Utilities
Compatible with LangChain v1+
Minimal Hybrid Retrieval Utilities
LangChain v1 Compatible
No HuggingFace dependencies
"""

from typing import List
import numpy as np
from rank_bm25 import BM25Okapi
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS


def hybrid_search(
    query: str,
    faiss_store: FAISS,
    docs: List[Document],
    alpha: float = 0.6,
    k: int = 30,
) -> List[Document]:
    """
    Hybrid retrieval combining:
    - Dense similarity search (FAISS)
    - Sparse BM25 keyword search

    alpha controls weighting:
        1.0 → only dense
        0.0 → only sparse
    """

    if not docs:
        return []

    # =========================
    # Dense Retrieval (FAISS)
    # =========================
    dense_results = faiss_store.similarity_search_with_score(query, k=k)

    dense_docs = [doc for doc, _ in dense_results]
    dense_scores = np.array([score for _, score in dense_results])

    # Convert FAISS distance → similarity
    if len(dense_scores) > 0:
        dense_scores = 1 - (
            (dense_scores - dense_scores.min())
            / (dense_scores.max() - dense_scores.min() + 1e-9)
        )

    # =========================
    # Sparse Retrieval (BM25)
    # =========================
    tokenized_corpus = [d.page_content.split() for d in docs]
    bm25 = BM25Okapi(tokenized_corpus)

    sparse_scores_full = bm25.get_scores(query.split())
    top_sparse_idx = np.argsort(sparse_scores_full)[::-1][:k]

    sparse_docs = [docs[i] for i in top_sparse_idx]
    sparse_scores = sparse_scores_full[top_sparse_idx]

    if len(sparse_scores) > 0:
        sparse_scores = (
            (sparse_scores - sparse_scores.min())
            / (sparse_scores.max() - sparse_scores.min() + 1e-9)
        )

    # =========================
    # Merge Scores
    # =========================
    combined = {}

    for doc, score in zip(dense_docs, dense_scores):
        combined[doc.page_content] = alpha * score

    for doc, score in zip(sparse_docs, sparse_scores):
        combined[doc.page_content] = combined.get(doc.page_content, 0) + (
            (1 - alpha) * score
        )

    # =========================
    # Sort Results
    # =========================
    sorted_docs = sorted(
        combined.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    return [Document(page_content=text) for text, _ in sorted_docs[:k]]


# from typing import List
# import numpy as np
# from rank_bm25 import BM25Okapi
# from langchain_core.documents import Document
# from langchain_community.vectorstores import FAISS
# from sentence_transformers import CrossEncoder
# from sklearn.decomposition import PCA
# from sentence_transformers import SentenceTransformer


# # ============================================================
# # HYBRID SEARCH (Dense + BM25)
# # ============================================================

# def hybrid_search(
#     query: str,
#     faiss_store: FAISS,
#     docs: List[Document],
#     embedding_model,
#     alpha: float = 0.5,
#     k: int = 30,
# ) -> List[Document]:
#     """
#     Combines FAISS dense retrieval with BM25 sparse retrieval.
#     """

#     # -------------------------
#     # Dense retrieval (FAISS)
#     # -------------------------
#     dense_results = faiss_store.similarity_search_with_score(query, k=k)

#     dense_docs = [doc for doc, _ in dense_results]
#     dense_scores = np.array([score for _, score in dense_results])

#     # Normalize dense scores (lower distance = better)
#     if len(dense_scores) > 0:
#         dense_scores = 1 - (dense_scores - dense_scores.min()) / (
#             dense_scores.max() - dense_scores.min() + 1e-9
#         )

#     # -------------------------
#     # Sparse retrieval (BM25)
#     # -------------------------
#     tokenized_corpus = [d.page_content.split() for d in docs]
#     bm25 = BM25Okapi(tokenized_corpus)

#     sparse_scores_full = bm25.get_scores(query.split())
#     top_sparse_idx = np.argsort(sparse_scores_full)[::-1][:k]
#     sparse_docs = [docs[i] for i in top_sparse_idx]
#     sparse_scores = sparse_scores_full[top_sparse_idx]

#     # Normalize sparse scores
#     if len(sparse_scores) > 0:
#         sparse_scores = (sparse_scores - sparse_scores.min()) / (
#             sparse_scores.max() - sparse_scores.min() + 1e-9
#         )

#     # -------------------------
#     # Merge scores
#     # -------------------------
#     combined_scores = {}

#     for doc, score in zip(dense_docs, dense_scores):
#         combined_scores[doc.page_content] = alpha * score

#     for doc, score in zip(sparse_docs, sparse_scores):
#         combined_scores[doc.page_content] = combined_scores.get(
#             doc.page_content, 0
#         ) + (1 - alpha) * score

#     # -------------------------
#     # Sort and return
#     # -------------------------
#     sorted_docs = sorted(
#         combined_scores.items(),
#         key=lambda x: x[1],
#         reverse=True,
#     )

#     return [Document(page_content=text) for text, _ in sorted_docs[:k]]


# # ============================================================
# # CROSS-ENCODER RERANKING
# # ============================================================

# # cross_encoder = CrossEncoder("BAAI/bge-reranker-base")

# _cross_encoder = None

# def get_cross_encoder():
#     global _cross_encoder
#     if _cross_encoder is None:
#         _cross_encoder = CrossEncoder("BAAI/bge-reranker-base")
#     return _cross_encoder



# def rerank(query: str, docs: List[Document], k: int = 20) -> List[Document]:
#     """
#     Re-rank documents using cross-encoder relevance scoring.
#     """
#     if not docs:
#         return []

#     pairs = [(query, d.page_content) for d in docs]
#     encoder = get_cross_encoder()
#     scores = encoder.predict(pairs)
#     # scores = cross_encoder.predict(pairs)

#     ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

#     return [doc for doc, _ in ranked[:k]]


# # ============================================================
# # OPTIONAL: PCA DIMENSION REDUCTION
# # ============================================================

# def apply_pca_to_embeddings(embeddings, n_components=256):
#     pca = PCA(n_components=n_components)
#     reduced = pca.fit_transform(embeddings)
#     return reduced, pca


# # ============================================================
# # OPTIONAL: ASYMMETRIC ENCODERS (Advanced)
# # ============================================================

# doc_encoder = SentenceTransformer("intfloat/e5-large-v2")
# query_encoder = SentenceTransformer("intfloat/e5-large-v2")


# def embed_docs_asymmetric(docs: List[Document]):
#     texts = [d.page_content for d in docs]
#     embeddings = doc_encoder.encode(texts, normalize_embeddings=True)
#     return embeddings


# def embed_query_asymmetric(query: str):
#     return query_encoder.encode([query], normalize_embeddings=True)[0]
