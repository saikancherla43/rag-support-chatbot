"""Answering layer (extractive).

This demo answers WITHOUT an LLM: it retrieves the top-k chunks and
synthesizes an answer by extracting the most relevant sentences, always
with citations back to the source chunks. Every claim in the answer is
traceable to a cited chunk — no hallucinated content.

PRODUCTION NOTE: the generation layer is pluggable. To produce abstractive
answers, swap ``synthesize()`` for a call to an LLM API (e.g. OpenAI), passing
the retrieved chunks as context with an instruction to answer only from the
context and cite chunk ids. Retrieval, chunking, and evals stay the same.
"""

from __future__ import annotations

import re

from embed import Index
from retrieve import search


def _split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def synthesize(query: str, results: list[tuple]) -> str:
    """Build an extractive summary from the top retrieved chunks."""
    query_terms = set(re.findall(r"\w+", query.lower()))
    picked: list[str] = []
    for chunk, _ in results:
        # score sentences by query-term overlap, keep the best two per chunk
        scored = sorted(
            _split_sentences(chunk.text),
            key=lambda s: len(set(re.findall(r"\w+", s.lower())) & query_terms),
            reverse=True,
        )
        picked.extend(scored[:2])
    # de-duplicate while preserving order, cap length
    seen, out = set(), []
    for s in picked:
        if s not in seen:
            seen.add(s)
            out.append(s)
        if len(out) >= 6:
            break
    return " ".join(out)


def answer(query: str, index: Index, k: int = 3) -> dict:
    results = search(query, index, k=k)
    return {
        "query": query,
        "summary": synthesize(query, results),
        "sources": [
            {
                "id": chunk.id,
                "doc": chunk.doc,
                "title": chunk.title,
                "section": chunk.section,
                "score": round(float(score), 3),
            }
            for chunk, score in results
        ],
    }


if __name__ == "__main__":
    idx = Index.load()
    ans = answer("how much does the growth plan cost?", idx)
    print("Q:", ans["query"])
    print("A:", ans["summary"])
    for s in ans["sources"]:
        print(f"  [{s['score']}] {s['title']} > {s['section']} ({s['id']})")
