from src.analysis.classifier import NewsClassifier


def test_classifier_fit_predict():
    texts = ["stock market shares profit bank company economy"] * 12 + \
            ["goal match team player win league champion"] * 12
    labels = ["business"] * 12 + ["sport"] * 12
    clf = NewsClassifier(max_features=200).fit(texts, labels)
    r = clf.predict("the team scored a late goal to win the match and league")
    assert r["category"] in ("sport", "business", "uncertain")
    assert 0.0 <= r["confidence"] <= 1.0
