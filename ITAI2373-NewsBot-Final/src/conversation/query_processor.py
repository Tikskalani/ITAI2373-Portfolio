"""Natural-language query routing for NewsBot 2.0 (Module D).

Detects intent and dispatches to the right component (classifier, sentiment, NER,
summarizer, semantic search, topic modeler). Keeps simple conversation history.
"""
from src.conversation.intent_classifier import IntentClassifier
from src.conversation.response_generator import ResponseGenerator


class QueryProcessor:
    def __init__(self, bot=None, summarizer=None, search=None, topic_modeler=None):
        self.intent_clf = IntentClassifier()
        self.responder = ResponseGenerator()
        self.bot = bot
        self.summarizer = summarizer
        self.search = search
        self.topic_modeler = topic_modeler
        self.history = []

    def process(self, query: str, article: str = None):
        intent = self.intent_clf.classify(query)
        self.history.append({"query": query, "intent": intent})
        result = {"note": "provide the required input for this intent"}
        try:
            if intent == "classify" and self.bot and article:
                result = self.bot.classifier.predict(article)
            elif intent == "sentiment" and self.bot and article:
                result = self.bot.sentiment.analyze(article)
            elif intent == "entities" and self.bot and article:
                result = self.bot.ner.extract(article)
            elif intent == "summarize" and self.summarizer and article:
                result = self.summarizer.summarize(article)
            elif intent == "search" and self.search is not None:
                result = self.search.search(query, k=3)
            elif intent == "topics" and self.topic_modeler is not None:
                result = self.topic_modeler.get_all_topics(6)
        except Exception as e:  # keep the interface robust in a live demo
            return {"intent": intent, "response": f"Sorry, I hit an error handling that: {e}", "raw": None}
        return {"intent": intent, "response": self.responder.format(intent, result), "raw": result}
