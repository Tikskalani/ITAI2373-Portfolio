"""Enhanced multi-class news classifier with an uncertainty guard (NewsBot 2.0)."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

from src.data_processing.text_preprocessor import TextPreprocessor


class NewsClassifier:
    """TF-IDF + Logistic Regression classifier with model comparison and a robustness guard.

    The guard returns 'uncertain' when the input has too few recognized vocabulary terms
    or the top probability is low, rather than forcing a confident wrong label.
    """
    MIN_KNOWN = 2
    MIN_CONFIDENCE = 0.35

    def __init__(self, max_features=5000, ngram_range=(1, 2), random_state=42):
        self.random_state = random_state
        self.pre = TextPreprocessor()
        self.vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=ngram_range,
                                          min_df=5, max_df=0.9, sublinear_tf=True)
        self.model = LogisticRegression(max_iter=1000, C=10)
        self.classes_ = None
        self._fitted = False

    def fit(self, texts, labels, preprocess=True):
        proc = self.pre.transform(texts) if preprocess else list(texts)
        X = self.vectorizer.fit_transform(proc)
        self.model.fit(X, labels)
        self.classes_ = self.model.classes_
        self.vocab_ = self.vectorizer.get_feature_names_out()
        self._fitted = True
        return self

    def predict(self, text):
        proc = self.pre.preprocess(text)
        v = self.vectorizer.transform([proc])
        known = int(v.nnz)
        probs = self.model.predict_proba(v)[0]
        order = probs.argsort()[::-1]
        top, conf = self.classes_[order[0]], float(probs[order[0]])
        arr = v.toarray().ravel()
        key_terms = [self.vocab_[i] for i in arr.argsort()[::-1][:6] if arr[i] > 0]
        if known < self.MIN_KNOWN:
            category, note = "uncertain", f"only {known} recognized words; paste a longer excerpt"
        elif conf < self.MIN_CONFIDENCE:
            category, note = "uncertain", f"low confidence; closest is {top} ({conf:.2f})"
        else:
            category, note = top, ""
        return {"category": category, "confidence": round(conf, 3),
                "runner_up": f"{self.classes_[order[1]]} ({probs[order[1]]:.2f})",
                "recognized_terms": known, "note": note, "key_terms": key_terms}

    def compare_models(self, texts, labels, preprocess=True, cv=5):
        """Train and evaluate four algorithms; return a results table sorted by test accuracy."""
        proc = self.pre.transform(texts) if preprocess else list(texts)
        Xtr_t, Xte_t, ytr, yte = train_test_split(proc, labels, test_size=0.2,
                                                  stratify=labels, random_state=self.random_state)
        vec = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=5, max_df=0.9, sublinear_tf=True)
        Xtr, Xte = vec.fit_transform(Xtr_t), vec.transform(Xte_t)
        models = {
            "Multinomial NB": MultinomialNB(),
            "Logistic Regression": LogisticRegression(max_iter=1000, C=10),
            "Linear SVM": LinearSVC(C=1),
            "Random Forest": RandomForestClassifier(n_estimators=120, n_jobs=-1, random_state=self.random_state),
        }
        rows = []
        for name, m in models.items():
            cv_scores = cross_val_score(m, Xtr, ytr, cv=cv, scoring="accuracy")
            m.fit(Xtr, ytr); pred = m.predict(Xte)
            rows.append({"model": name, "cv_accuracy": round(cv_scores.mean(), 3),
                         "test_accuracy": round(accuracy_score(yte, pred), 3),
                         "macro_f1": round(f1_score(yte, pred, average="macro"), 3)})
        return sorted(rows, key=lambda r: r["test_accuracy"], reverse=True)
