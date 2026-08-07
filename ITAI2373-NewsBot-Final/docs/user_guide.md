# NewsBot 2.0 — User Guide

This guide is for someone who wants to run NewsBot and read its output. No machine
learning background is needed.

## What NewsBot does

Paste in a news article and NewsBot tells you:
- the category (business, entertainment, politics, sport, or tech) and how
  confident it is,
- the overall sentiment and the dominant emotion,
- the people, organizations, places, dates, and money it found,
- a short summary,
- and, on request, similar articles and the broad topics in the collection.

You can also just ask it questions in plain English, like "what is the sentiment?"
or "who is mentioned?".

## Install

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Use it from Python

```python
import sys; sys.path.append(".")
import pandas as pd
from src.newsbot import NewsBot
from src.language_models.summarizer import Summarizer
from src.language_models.embeddings import SemanticSearch

df = pd.read_csv("data/raw/newsbot_bbc.csv")
bot = NewsBot().train(df["text"], df["category"])

print(bot.analyze("The Nasdaq fell as Apple shares dropped over worries about costs."))
print(Summarizer().summarize(df["text"].iloc[0], n_sentences=2))
print(SemanticSearch().index(df["text"]).search("football championship final", k=3))
```

## Use the web app

```bash
python app.py
# open http://localhost:5000
```

The dashboard has three panels:
- Analyze an article: paste text, get category, sentiment, entities, and summary.
- Ask NewsBot: type a question about the article you just analyzed.
- Find similar articles: type a phrase and get the closest matches from the corpus.

## Run in Google Colab

Open any notebook in `notebooks/`, choose Runtime > Run all. The notebooks install
their own dependencies in the first cell, so no local setup is needed.

## FAQ

Why does it say "uncertain"?
The model was trained on BBC News and only knows five categories. If you paste text
that is too short, empty, or clearly outside those topics, it reports `uncertain`
on purpose instead of guessing. That is the safe behavior for a real tool.

Why did a profit warning score as positive?
Lexicon sentiment reads surface words. Financial language often fools it. The
technical documentation lists this as a known limitation and points to FinBERT as
the fix.

Do I need a GPU or API keys?
No. The default install runs on CPU with no keys. Optional transformer features and
translation use free backends and are clearly marked as optional.

Translation returns an error.
Translation uses a free online backend and needs a network connection. Check your
connection and retry, or work with English text only.
