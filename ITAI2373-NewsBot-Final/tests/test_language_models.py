from src.language_models.summarizer import Summarizer
from src.language_models.embeddings import SemanticSearch


def test_extractive_summary():
    text = ("Banks reported record profits this quarter. "
            "The football team won the match last night. "
            "Investors reacted to the market news today. "
            "The award went to the best actor at the ceremony.")
    s = Summarizer(method="extractive").summarize(text, n_sentences=2)
    assert isinstance(s, str) and len(s) > 0


def test_semantic_search_ranks_relevant_first():
    docs = ["bank market money profit economy",
            "football match team goal league",
            "film award actor movie ceremony",
            "election party vote government"]
    ss = SemanticSearch(backend="tfidf").index(docs)
    hits = ss.search("goal team football league", k=2)
    assert hits[0][0] == 1
