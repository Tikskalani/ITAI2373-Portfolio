from src.conversation.intent_classifier import IntentClassifier
from src.conversation.query_processor import QueryProcessor


def test_intent_detection():
    ic = IntentClassifier()
    assert ic.classify("what is the sentiment of this article") == "sentiment"
    assert ic.classify("find news about elections") == "search"
    assert ic.classify("give me a summary") == "summarize"


def test_query_processor_runs_without_backend():
    out = QueryProcessor().process("summarize this")
    assert "intent" in out and "response" in out
