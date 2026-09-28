"""Embeddings: sentence-transformers (all-MiniLM-L6-v2) with TF-IDF fallback.

The primary backend is the ``all-MiniLM-L6-v2`` embedding model, a standard
choice for retrieval demos (384-dim, fast, strong semantic matching). If the
model cannot be downloaded in the current environment, we fall back to
TF-IDF vectors via scikit-learn so the pipeline still runs end-to-end.
The active backend is recorded in the saved index — retrieval adapts
automatically. Nothing here is faked: ``backend`` in the index tells you
exactly which encoder produced the vectors.
"""

from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np

MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_PATH = Path(__file__).parent / "index.pkl"


def _model_source() -> str:
    """Model id, or a local directory (env ST_MODEL_DIR) for offline/restricted
    networks — e.g. weights pre-fetched with curl into ./models/."""
    import os

    return os.environ.get("ST_MODEL_DIR", MODEL_NAME)


def _try_sentence_transformer():
    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(_model_source())  # downloads on first run
        return model
    except Exception as exc:  # no network / no torch -> fall back
        print(f"[embed] sentence-transformers unavailable ({exc}); using TF-IDF fallback")
        return None


class Index:
    def __init__(self, chunks, backend: str, encoder, matrix):
        self.chunks = chunks
        self.backend = backend
        self.encoder = encoder      # SentenceTransformer or TfidfVectorizer
        self.matrix = matrix        # np.ndarray (dense) or sparse TF-IDF matrix

    def encode_query(self, query: str):
        if self.backend == "sbert":
            vec = self.encoder.encode([query], normalize_embeddings=True)
            return np.asarray(vec, dtype=np.float32)
        return self.encoder.transform([query])

    def save(self, path: Path = INDEX_PATH) -> None:
        with open(path, "wb") as f:
            pickle.dump(
                {"chunks": self.chunks, "backend": self.backend,
                 "encoder": self.encoder, "matrix": self.matrix}, f)
        print(f"[embed] saved index ({self.backend}, {len(self.chunks)} chunks) -> {path}")

    @classmethod
    def load(cls, path: Path = INDEX_PATH) -> "Index":
        with open(path, "rb") as f:
            d = pickle.load(f)
        return cls(d["chunks"], d["backend"], d["encoder"], d["matrix"])


def build_index(chunks) -> Index:
    texts = [c.text for c in chunks]
    model = _try_sentence_transformer()
    if model is not None:
        matrix = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        matrix = np.asarray(matrix, dtype=np.float32)
        return Index(chunks, backend="sbert", encoder=model, matrix=matrix)

    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(texts)
    return Index(chunks, backend="tfidf", encoder=vectorizer, matrix=matrix)


if __name__ == "__main__":
    from ingest import ingest

    chunks = ingest(Path(__file__).parent.parent / "corpus")
    build_index(chunks).save()
