# NewsBot Intelligence System 2.0

**ITAI 2373 - Natural Language Processing | Final Project**

A production-style, modular news-analysis platform that extends the midterm NewsBot into a full NLP system: advanced content analysis, language understanding and generation, multilingual intelligence, a conversational interface, and a Flask web frontend.

> Author: Trilok Kalani
> Live demo (interactive, no install): https://tikskalani.github.io/ITAI2373-Portfolio/
 | Group: Solo | Builds on: [ITAI2373-NewsBot-Midterm](../ITAI2373-NewsBot-Midterm)

---

## The four modules

| Module | Capability | Status |
|---|---|---|
| **A. Advanced Content Analysis** | Classification (confidence + uncertainty guard), sentiment/emotion, NER, topic modeling (LDA **and** NMF) | Implemented |
| **B. Language Understanding & Generation** | Summarization (extractive + optional transformer), semantic search (TF-IDF + optional SBERT), content enhancement, query expansion | Implemented |
| **C. Multilingual Intelligence** | Language detection (langdetect), translation (deep-translator), cross-lingual analyze-in-English | Implemented |
| **D. Conversational Interface** | Intent detection, natural-language query routing, response generation, context history | Implemented |
| **Web app (bonus)** | Flask dashboard: analyze, ask, semantic search, topics | Implemented |

Every component works out of the box with lightweight defaults (extractive summaries, TF-IDF search). Optional transformer upgrades (abstractive summarization, dense SBERT embeddings) are lazy-loaded and documented, so nothing forces a heavy install.

## Architecture

```
ITAI2373-NewsBot-Final/
├── README.md
├── requirements.txt
├── app.py                          # Flask web application (bonus)
├── config/                         # settings.py, api_keys_template.txt
├── src/
│   ├── newsbot.py                  # top-level facade (classify + sentiment + entities)
│   ├── data_processing/            # text_preprocessor, feature_extractor, data_validator
│   ├── analysis/                   # classifier, sentiment_analyzer, ner_extractor, topic_modeler
│   ├── language_models/            # summarizer, embeddings (semantic search), generator
│   ├── multilingual/               # language_detector, translator, cross_lingual_analyzer
│   ├── conversation/               # intent_classifier, query_processor, response_generator
│   └── utils/                      # visualization, evaluation, export
├── templates/ + static/           # web app UI
├── notebooks/                      # 01..07, one per stage
├── tests/                          # pytest suite (8 tests)
├── data/                           # raw / processed / models / results
├── docs/                           # technical, user, API, deployment, web_app docs
└── reports/                        # executive summary, technical report, slides
```

## Quick start

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Use the library:

```python
import sys; sys.path.append(".")
import pandas as pd
from src.newsbot import NewsBot
from src.language_models.summarizer import Summarizer
from src.language_models.embeddings import SemanticSearch

df = pd.read_csv("data/raw/newsbot_bbc.csv")
bot = NewsBot().train(df["text"], df["category"])
print(bot.analyze("Apple unveiled a new AI chip, intensifying competition with Nvidia."))
print(Summarizer().summarize(df["text"].iloc[0], n_sentences=2))
print(SemanticSearch().index(df["text"]).search("football championship final", k=3))
```

Run the web app:

```bash
python app.py      # then open http://localhost:5000
```

## Testing

```bash
pytest tests/ -q      # 8 passing
```


## Final deliverables

| Deliverable | File |
|---|---|
| Technical documentation | reports/FP_TechnicalDoc_TrilokKalani_SOLO_ITAI2373.pdf |
| Executive summary | reports/FP_ExecutiveSummary_TrilokKalani_SOLO_ITAI2373.pdf |
| Reflective journal (3 pages) | reports/FP_ReflectiveJournal_SOLO_ITAI2373.pdf |
| Presentation deck | reports/FP_Presentation_TrilokKalani_SOLO_ITAI2373.pptx |
| Video presentation | recorded from VIDEO_SCRIPT.md (link added after recording) |

Notebooks 01-07 in `notebooks/` run end-to-end (they auto-locate the repo, or clone it on a fresh Colab) and are saved with their outputs.

## What carries over from the midterm

The midterm delivered a working preprocessing to TF-IDF to classification pipeline (97.5% test accuracy), sentiment/emotion, NER with a domain EntityRuler, LDA topic modeling, and a Gradio dashboard. Those are refactored here into clean `src/` classes and are the foundation the four advanced modules and the web app extend.

## Individual contributions
Trilok Kalani (solo). I designed the modular architecture, ported and refactored the midterm pipeline into `src/`, implemented the four advanced modules and the Flask web app, and wrote the tests. See `docs/individual_contributions.md`.

## AI-use disclosure
I used an AI assistant for code implementation, refactoring, debugging, and drafting. I chose the architecture and methods, run and review the code, verify outputs, and am responsible for the design and interpretation.

## References
- BBC News dataset: D. Greene and P. Cunningham, ICML 2006.
- spaCy, scikit-learn, NLTK, TextBlob, Flask; (optional) Hugging Face Transformers, Sentence-Transformers; langdetect, deep-translator.
