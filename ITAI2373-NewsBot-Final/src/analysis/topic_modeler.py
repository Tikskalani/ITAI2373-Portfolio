"""Topic modeling (LDA / NMF) for NewsBot 2.0 content discovery."""
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF


class TopicModeler:
    """Discover latent topics with LDA or NMF and expose per-topic top words.

    Mirrors the interface suggested in the project spec:
        fit_transform(documents), get_topic_words(topic_id), visualize_topics().
    """

    def __init__(self, n_topics=5, method="lda", max_features=1000, random_state=42):
        self.n_topics = n_topics
        self.method = method.lower()
        self.random_state = random_state
        if self.method == "nmf":
            self.vectorizer = TfidfVectorizer(max_features=max_features, min_df=5, max_df=0.9,
                                              stop_words="english", token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b")
            self.model = NMF(n_components=n_topics, random_state=random_state, init="nndsvda", max_iter=400)
        else:
            self.vectorizer = CountVectorizer(max_features=max_features, min_df=5, max_df=0.9,
                                              stop_words="english", token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b")
            self.model = LatentDirichletAllocation(n_components=n_topics, random_state=random_state,
                                                   learning_method="batch", max_iter=15)
        self.vocab_ = None

    def fit_transform(self, documents):
        """Train the topic model and return the document-topic matrix."""
        X = self.vectorizer.fit_transform(documents)
        W = self.model.fit_transform(X)
        self.vocab_ = np.array(self.vectorizer.get_feature_names_out())
        return W

    def get_topic_words(self, topic_id, n_words=10):
        """Top words for a specific topic."""
        comp = self.model.components_[topic_id]
        return list(self.vocab_[comp.argsort()[::-1][:n_words]])

    def get_all_topics(self, n_words=8):
        return {k: self.get_topic_words(k, n_words) for k in range(self.n_topics)}

    def visualize_topics(self, n_words=8):
        """Compact text view of the discovered topics (swap in pyLDAvis for interactive)."""
        for k in range(self.n_topics):
            print(f"Topic {k}: " + ", ".join(self.get_topic_words(k, n_words)))
