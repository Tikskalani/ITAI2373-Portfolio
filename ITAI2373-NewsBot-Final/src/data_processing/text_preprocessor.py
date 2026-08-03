"""Text preprocessing for NewsBot 2.0 (ported and enhanced from the midterm).

Fast, dependency-light normalization used across the whole pipeline. The canonical
tunable values live in config/settings.py; sensible defaults are inlined here so the
class works when imported from anywhere.
"""
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def _ensure_nltk():
    for path, pkg in [("corpora/stopwords", "stopwords"), ("corpora/wordnet", "wordnet"),
                      ("corpora/omw-1.4", "omw-1.4")]:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(pkg, quiet=True)


class TextPreprocessor:
    """Clean, tokenize, stop-word filter and lemmatize raw article text."""

    TOKEN_RE = re.compile(r"[a-z]+")

    def __init__(self, min_token_len: int = 2):
        _ensure_nltk()
        self.stopwords = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()
        self.min_token_len = min_token_len

    def preprocess(self, text: str) -> str:
        """Return a space-joined string of cleaned, lemmatized content tokens."""
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r"http\S+|www\.\S+", " ", text)   # URLs
        text = re.sub(r"\S+@\S+", " ", text)            # emails
        tokens = self.TOKEN_RE.findall(text)            # letters only -> drops digits/punct
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens
                  if t not in self.stopwords and len(t) > self.min_token_len]
        return " ".join(tokens)

    def transform(self, texts):
        """Preprocess an iterable of documents."""
        return [self.preprocess(t) for t in texts]

    __call__ = preprocess
