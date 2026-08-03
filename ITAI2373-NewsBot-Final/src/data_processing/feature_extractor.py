"""TF-IDF feature extraction for NewsBot 2.0."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class FeatureExtractor:
    """Wrap a tuned TfidfVectorizer and expose category-level term analysis."""

    def __init__(self, max_features=5000, ngram_range=(1, 2), min_df=5, max_df=0.9):
        self.vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=ngram_range,
                                          min_df=min_df, max_df=max_df, sublinear_tf=True)

    def fit_transform(self, documents):
        return self.vectorizer.fit_transform(documents)

    def transform(self, documents):
        return self.vectorizer.transform(documents)

    @property
    def feature_names(self):
        return np.array(self.vectorizer.get_feature_names_out())

    def top_terms(self, X, labels, category, n=12):
        """Mean TF-IDF top terms for one category."""
        labels = np.asarray(labels)
        idx = np.where(labels == category)[0]
        means = np.asarray(X[idx].mean(axis=0)).ravel()
        order = means.argsort()[::-1][:n]
        return list(zip(self.feature_names[order], means[order]))
