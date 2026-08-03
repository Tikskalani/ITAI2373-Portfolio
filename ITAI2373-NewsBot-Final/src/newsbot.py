"""NewsBot 2.0 top-level facade tying the analysis modules together (integration layer)."""
from src.analysis.classifier import NewsClassifier
from src.analysis.sentiment_analyzer import SentimentAnalyzer
from src.analysis.ner_extractor import NERExtractor


class NewsBot:
    """One object that classifies, scores sentiment, and extracts entities for any article."""

    def __init__(self, use_domain_rules=False):
        self.classifier = NewsClassifier()
        self.sentiment = SentimentAnalyzer()
        self.ner = NERExtractor(use_domain_rules=use_domain_rules)
        self._trained = False

    def train(self, texts, labels):
        self.classifier.fit(texts, labels)
        self._trained = True
        return self

    def analyze(self, text):
        return {
            "classification": self.classifier.predict(text) if self._trained else {"note": "call train() first"},
            "sentiment": self.sentiment.analyze(text),
            "entities": self.ner.extract(text),
        }
