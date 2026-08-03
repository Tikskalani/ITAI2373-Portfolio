"""Semantic search for NewsBot 2.0 (Module B).

Backends:
- "tfidf" (default): TF-IDF vector cosine similarity. No heavy dependencies.
- "sbert": dense sentence-transformer embeddings (lazy, needs sentence-transformers).
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticSearch:
    def __init__(self, backend="tfidf", model="sentence-transformers/all-MiniLM-L6-v2"):
        self.backend = backend
        self.model_name = model
        self._docs = None
        self._matrix = None
        self._vec = None
        self._sbert = None

    def index(self, documents):
        self._docs = list(documents)
        if self.backend == "sbert":
            self._ensure_sbert()
            self._matrix = self._sbert.encode(self._docs, convert_to_numpy=True, normalize_embeddings=True)
        else:
            self._vec = TfidfVectorizer(stop_words="english", max_features=20000)
            self._matrix = self._vec.fit_transform(self._docs)
        return self

    def search(self, query, k=5):
        if self.backend == "sbert":
            q = self._sbert.encode([query], convert_to_numpy=True, normalize_embeddings=True)
            sims = self._matrix @ q[0]
        else:
            sims = cosine_similarity(self._vec.transform([query]), self._matrix).ravel()
        idx = sims.argsort()[::-1][:k]
        return [(int(i), round(float(sims[i]), 3), self._docs[i][:200]) for i in idx]

    def _ensure_sbert(self):
        if self._sbert is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as e:
                raise ImportError("Install sentence-transformers for backend='sbert', or use backend='tfidf'.") from e
            self._sbert = SentenceTransformer(self.model_name)
