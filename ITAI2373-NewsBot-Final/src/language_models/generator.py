"""Content enhancement and query expansion for NewsBot 2.0 (Module B)."""
import nltk


def _ensure_wordnet():
    for path, pkg in [("corpora/wordnet", "wordnet"), ("corpora/omw-1.4", "omw-1.4")]:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(pkg, quiet=True)


class ContentGenerator:
    """Turn structured analysis into readable insight text, and expand search queries."""

    def enhance(self, analysis: dict) -> str:
        cls = analysis.get("classification", {})
        sen = analysis.get("sentiment", {})
        ents = analysis.get("entities", [])
        who = ", ".join(t for t, l in ents[:5]) if ents else "no notable entities"
        return (f"This article reads as {cls.get('category', 'unknown')} news with a "
                f"{sen.get('label', 'neutral')} tone. Key entities include {who}.")

    @staticmethod
    def expand_query(query, per_word=2):
        """Add WordNet synonyms to a query to improve search recall."""
        _ensure_wordnet()
        from nltk.corpus import wordnet
        expanded = set(query.lower().split())
        for w in query.lower().split():
            for syn in wordnet.synsets(w)[:2]:
                for lemma in syn.lemmas()[:per_word]:
                    name = lemma.name().replace("_", " ")
                    if name.isalpha():
                        expanded.add(name)
        return " ".join(sorted(expanded))
