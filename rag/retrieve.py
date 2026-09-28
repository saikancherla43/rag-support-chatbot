"""Retrieval: cosine-similarity top-k search over the chunk index.

Works with both backends produced by embed.py:
- sbert: dense normalized vectors -> cosine similarity = dot product
- tfidf: sparse TF-IDF vectors -> cosine via sklearn pairwise
"""

from __future__ import annotations

import numpy as np

from embed import Index


def search(query: str, index: Index, k: int = 3) -> list[tuple]:
    """Return top-k (chunk, score) pairs sorted by descending similarity."""
    q = index.encode_query(query)
    if index.backend == "sbert":
        scores = (index.matrix @ q[0]).tolist()
    else:
        from sklearn.metrics.pairwise import cosine_similarity

        scores = cosine_similarity(q, index.matrix)[0].tolist()
    ranked = sorted(zip(index.chunks, scores), key=lambda t: t[1], reverse=True)
    return ranked[:k]


if __name__ == "__main__":
    idx = Index.load()
    for chunk, score in search("how much does the growth plan cost?", idx, k=3):
        print(f"{score:.3f}  {chunk.id} [{chunk.section}]")
