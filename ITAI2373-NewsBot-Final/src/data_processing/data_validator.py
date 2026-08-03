"""Data quality checks for NewsBot 2.0."""
import pandas as pd


class DataValidator:
    """Validate and clean a news DataFrame before it enters the pipeline."""

    def __init__(self, text_col="text", category_col="category", min_words=5):
        self.text_col = text_col
        self.category_col = category_col
        self.min_words = min_words

    def validate(self, df: pd.DataFrame) -> dict:
        wc = df[self.text_col].fillna("").str.split().str.len()
        report = {
            "n_rows": len(df),
            "missing_text": int(df[self.text_col].isna().sum()),
            "missing_category": int(df[self.category_col].isna().sum()),
            "short_articles": int((wc < self.min_words).sum()),
            "class_counts": df[self.category_col].value_counts().to_dict(),
            "n_classes": int(df[self.category_col].nunique()),
        }
        report["is_valid"] = (report["missing_text"] == 0 and report["missing_category"] == 0
                              and report["n_classes"] >= 2 and report["short_articles"] == 0)
        return report

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.dropna(subset=[self.text_col, self.category_col]).copy()
        out = out[out[self.text_col].str.split().str.len() >= self.min_words]
        return out.reset_index(drop=True)
