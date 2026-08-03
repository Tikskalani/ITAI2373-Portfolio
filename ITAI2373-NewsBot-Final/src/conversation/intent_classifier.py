"""Rule-based intent detection for news queries (NewsBot 2.0, Module D).

Deliberately transparent and dependency-free; can be upgraded to an ML classifier.
"""


class IntentClassifier:
    INTENTS = {
        "classify":  ["classify", "category", "what kind", "topic of", "what is this"],
        "sentiment": ["sentiment", "positive", "negative", "tone", "feel", "mood"],
        "entities":  ["who", "entities", "people", "organizations", "companies", "where"],
        "summarize": ["summary", "summarize", "tldr", "shorten", "brief"],
        "search":    ["find", "show me", "search", "articles about", "news about"],
        "topics":    ["topics", "themes", "trends", "what topics"],
    }

    def classify(self, query: str) -> str:
        q = (query or "").lower()
        for intent, keywords in self.INTENTS.items():
            if any(k in q for k in keywords):
                return intent
        return "unknown"
