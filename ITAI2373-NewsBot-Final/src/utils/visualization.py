"""Reusable plotting helpers for NewsBot 2.0."""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import confusion_matrix


def plot_confusion(y_true, y_pred, labels, title="Confusion Matrix"):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.xlabel("Predicted"); plt.ylabel("Actual"); plt.title(title); plt.tight_layout()
    return plt.gcf()


def plot_class_balance(labels, title="Articles per category"):
    plt.figure(figsize=(7, 4))
    pd.Series(list(labels)).value_counts().sort_index().plot(
        kind="bar", color=sns.color_palette("Set2"), title=title)
    plt.ylabel("count"); plt.tight_layout()
    return plt.gcf()
