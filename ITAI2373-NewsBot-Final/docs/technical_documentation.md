# NewsBot Intelligence System 2.0 — Technical Documentation

Author: Trilok Kalani | Course: ITAI 2373 | Group: SOLO
Builds on: ITAI2373-NewsBot-Midterm

## 1. Overview

NewsBot 2.0 is a modular news-analysis platform. It takes raw article text and
returns structured intelligence: category with a calibrated confidence, sentiment
and emotion, named entities, an extractive summary, semantic-search matches, and
discovered topics. A conversational layer maps plain-language questions onto those
capabilities, and a Flask web app exposes the whole thing through a browser.

The midterm delivered a single notebook that reached 97.5% test accuracy on BBC
News. The final refactors that pipeline into a `src/` Python package, adds four
advanced modules (topic modeling with LDA and NMF, summarization and semantic
search, multilingual analysis, and a conversational interface), wraps it in a
test suite, and ships a web frontend.

## 2. Architecture

```
                          ┌──────────────────────────┐
   raw article text  ───► │        NewsBot           │  facade
                          │  classify + sentiment +  │
                          │       entities           │
                          └────────────┬─────────────┘
                                       │
   ┌───────────────┬───────────────────┼───────────────────┬───────────────┐
   ▼               ▼                    ▼                   ▼               ▼
data_processing  analysis          language_models     multilingual    conversation
preprocessor     classifier        summarizer          detector        intent_classifier
feature_extract  sentiment         embeddings(search)  translator      query_processor
validator        ner_extractor     generator           cross_lingual   response_generator
                 topic_modeler
                                       │
                                       ▼
                            app.py  (Flask web UI)
                       /  /analyze  /query  /similar  /topics
```

Design principle: parse and vectorize once, reuse everywhere. The classifier owns
the fitted TF-IDF vectorizer; semantic search and topic modeling keep their own
vectorizers because they are tuned differently (search favors recall, the
classifier favors precision on the five known categories).

### 2.1 Module A — Advanced Content Analysis
- `analysis/classifier.py` — `NewsClassifier`. TF-IDF (unigrams + bigrams,
  `sublinear_tf`, tuned `min_df`/`max_df`) into Logistic Regression. Reports the
  winning category, its probability, the runner-up, and how many in-vocabulary
  terms it recognized. An uncertainty guard returns `uncertain` when the input
  has fewer than 2 recognized terms or the top probability is below 0.35, so the
  system refuses to force a label on empty or out-of-scope text. `compare_models`
  benchmarks Naive Bayes, Logistic Regression, Linear SVM, and Random Forest with
  cross-validation.
- `analysis/sentiment_analyzer.py` — VADER compound score plus TextBlob polarity
  and subjectivity, and a transparent 8-emotion lexicon (joy, anger, fear,
  sadness, surprise, disgust, trust, anticipation).
- `analysis/ner_extractor.py` — spaCy `en_core_web_sm` entities, with an optional
  EntityRuler (`use_domain_rules=True`) that corrects domain names such as Nvidia,
  OpenAI, and Manchester United.
- `analysis/topic_modeler.py` — `TopicModeler(method="lda"|"nmf")` over a
  CountVectorizer (LDA) or TF-IDF (NMF) matrix; exposes per-topic top words and a
  bar-chart visualization.

### 2.2 Module B — Language Understanding and Generation
- `language_models/summarizer.py` — extractive by default: sentences are scored by
  mean TF-IDF salience and the top n are returned in original order. An abstractive
  path (`method="abstractive"`) lazy-loads a DistilBART model only if requested, so
  the default install stays light.
- `language_models/embeddings.py` — `SemanticSearch(backend="tfidf")` ranks a
  corpus by cosine similarity to a query; an optional `sbert` backend swaps in
  sentence-transformer dense vectors.
- `language_models/generator.py` — `ContentGenerator.enhance` turns an analysis
  dict into a readable brief; `expand_query` adds WordNet synonyms to widen search.

### 2.3 Module C — Multilingual Intelligence
- `multilingual/language_detector.py` — langdetect wrapper.
- `multilingual/translator.py` — deep-translator (Google backend) to a target
  language, default English.
- `multilingual/cross_lingual_analyzer.py` — detect, translate to English, then run
  the standard English pipeline, so a Spanish or French article gets the same
  classification and sentiment treatment.

### 2.4 Module D — Conversational Interface
- `conversation/intent_classifier.py` — rule-based intent detection over six
  intents: classify, sentiment, entities, summarize, search, topics.
- `conversation/query_processor.py` — dispatches a query (and optional article) to
  the right component and returns a structured result.
- `conversation/response_generator.py` — formats that result into natural language.

## 3. Data

BBC News, 2,225 full-text articles across business, entertainment, politics, sport,
and tech. Stored at `data/raw/newsbot_bbc.csv`. The classifier fits its vectorizer
on the training split only, so there is no leakage into evaluation.

## 4. Key design decisions

1. Lightweight defaults, heavy options. Extractive summarization and TF-IDF search
   work with the base install. Transformer summarization and SBERT embeddings are
   lazy-loaded and documented, so nothing forces a multi-gigabyte download.
2. Honest uncertainty. The classifier is trained on 2004-2005 BBC news. Rather than
   confidently mislabel modern or off-topic input, it reports `uncertain`. This is
   the behavior a real monitoring tool needs.
3. Separation of concerns. Each capability is a small class with a single job, so
   components are testable in isolation and reusable from the notebooks, the tests,
   and the web app alike.

## 5. Testing

`pytest tests/ -q` runs 8 tests spanning preprocessing, classification, topic
modeling, language models, the conversational layer, and an end-to-end integration
test. The web app is covered by a Flask test client that asserts the routes return
200 with valid JSON.

## 6. Known limitations

- The small spaCy model makes occasional NER errors; `en_core_web_trf` would help.
- Lexicon sentiment misreads financial framing (a profit warning can score
  positive); a finance-tuned model such as FinBERT would be more reliable.
- Translation quality depends on the free Google backend and the network.
- The classifier's world knowledge is fixed to the training corpus vocabulary.

## 7. Repository map

See README.md for the full tree. The four advanced modules live under
`src/language_models`, `src/multilingual`, and `src/conversation`; the analysis
core is under `src/analysis`; the web app is `app.py` with `templates/` and
`static/`.
