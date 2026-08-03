"""Model evaluation helpers for NewsBot 2.0."""
from sklearn.metrics import classification_report, accuracy_score, f1_score


def evaluate(y_true, y_pred):
    return {
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "macro_f1": round(f1_score(y_true, y_pred, average="macro"), 4),
        "report": classification_report(y_true, y_pred),
    }
