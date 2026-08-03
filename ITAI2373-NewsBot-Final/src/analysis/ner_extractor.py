"""Named entity recognition for NewsBot 2.0 (spaCy, with optional domain rules)."""
from collections import Counter
import spacy

DEFAULT_KEEP = {"PERSON", "ORG", "GPE", "DATE", "MONEY", "NORP", "LOC", "EVENT", "PERCENT", "CARDINAL"}
DOMAIN_PATTERNS = [
    {"label": "ORG", "pattern": "Nvidia"}, {"label": "ORG", "pattern": "OpenAI"}, {"label": "ORG", "pattern": "HSBC"},
    {"label": "ORG", "pattern": [{"LOWER": "manchester"}, {"LOWER": "united"}]},
    {"label": "FAC", "pattern": [{"LOWER": "old"}, {"LOWER": "trafford"}]},
]


class NERExtractor:
    """Extract and analyze named entities, optionally boosted with domain patterns."""

    def __init__(self, model="en_core_web_sm", keep=None, use_domain_rules=False):
        try:
            self.nlp = spacy.load(model)
        except OSError:
            from spacy.cli import download
            download(model); self.nlp = spacy.load(model)
        self.keep = keep or DEFAULT_KEEP
        if use_domain_rules and "entity_ruler" not in self.nlp.pipe_names:
            ruler = self.nlp.add_pipe("entity_ruler", before="ner")
            ruler.add_patterns(DOMAIN_PATTERNS)

    def extract(self, text):
        return [(e.text, e.label_) for e in self.nlp(text).ents if e.label_ in self.keep]

    def label_counts(self, texts):
        counts = Counter()
        for doc in self.nlp.pipe(list(texts), batch_size=64):
            counts.update(e.label_ for e in doc.ents if e.label_ in self.keep)
        return dict(counts)
