"""Summarization for NewsBot 2.0 (Module B).

Two backends:
- "extractive" (default): TF-IDF sentence ranking. No heavy dependencies, runs anywhere.
- "abstractive": a pre-trained transformer (distilbart), loaded lazily (needs transformers + torch).
"""
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


class Summarizer:
    def __init__(self, method="extractive", model="sshleifer/distilbart-cnn-12-6"):
        self.method = method
        self.model_name = model
        self._pipe = None

    def summarize(self, text, n_sentences=3, max_length=130, min_length=30):
        text = (text or "").strip()
        if not text:
            return ""
        if self.method == "abstractive":
            return self._abstractive(text, max_length, min_length)
        return self.extractive(text, n_sentences)

    @staticmethod
    def extractive(text, n_sentences=3):
        """Rank sentences by summed TF-IDF weight and return the top ones in original order."""
        sents = [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]
        if len(sents) <= n_sentences:
            return " ".join(sents)
        X = TfidfVectorizer(stop_words="english").fit_transform(sents)
        scores = np.asarray(X.sum(axis=1)).ravel()
        top = sorted(sorted(range(len(sents)), key=lambda i: scores[i], reverse=True)[:n_sentences])
        return " ".join(sents[i] for i in top)

    def _abstractive(self, text, max_length, min_length):
        if self._pipe is None:
            try:
                from transformers import pipeline
            except ImportError as e:
                raise ImportError("Install transformers + torch for abstractive mode, or use method='extractive'.") from e
            self._pipe = pipeline("summarization", model=self.model_name)
        return self._pipe(text[:3000], max_length=max_length, min_length=min_length, do_sample=False)[0]["summary_text"]
