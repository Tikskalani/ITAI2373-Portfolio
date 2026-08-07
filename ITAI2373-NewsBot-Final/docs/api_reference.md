# NewsBot 2.0 — API Reference

All classes are importable from their module path under `src/`. Add the repo root
to `sys.path` (or install the package) first.

## src.newsbot

### `NewsBot(use_domain_rules=False)`
Top-level facade composing classification, sentiment, and entities.
- `train(texts, labels) -> NewsBot` — fits the classifier; returns self for chaining.
- `analyze(text) -> dict` — returns `{classification, sentiment, entities}`.

```python
from src.newsbot import NewsBot
bot = NewsBot(use_domain_rules=True).train(df["text"], df["category"])
bot.analyze("Apple unveiled a new AI chip, intensifying competition with Nvidia.")
```

## src.analysis.classifier

### `NewsClassifier(max_features=5000, ngram_range=(1,2), random_state=42)`
- `fit(texts, labels, preprocess=True) -> self`
- `predict(text) -> dict` — keys: `category`, `confidence`, `runner_up`,
  `recognized_terms`, `note`, `key_terms`. Returns `category="uncertain"` when the
  input has fewer than 2 recognized terms or confidence < 0.35.
- `compare_models(texts, labels, preprocess=True, cv=5) -> dict` — cross-validated
  accuracy for Naive Bayes, Logistic Regression, Linear SVM, Random Forest.

## src.analysis.sentiment_analyzer

### `SentimentAnalyzer()`
- `analyze(text) -> dict` — keys: `compound`, `label`, `polarity`, `subjectivity`,
  `emotion`.
- `detect_emotion(text) -> str` — dominant emotion from the 8-emotion lexicon.

## src.analysis.ner_extractor

### `NERExtractor(model="en_core_web_sm", keep=None, use_domain_rules=False)`
- `extract(text) -> list[tuple[str, str]]` — `(entity_text, label)` pairs.
- `label_counts(texts) -> dict` — entity-label frequency across a corpus.

## src.analysis.topic_modeler

### `TopicModeler(n_topics=5, method="lda", max_features=1000, random_state=42)`
- `fit_transform(documents) -> np.ndarray` — document-topic matrix.
- `get_topic_words(topic_id, n_words=10) -> list[str]`
- `get_all_topics(n_words=8) -> dict[int, list[str]]`
- `visualize_topics(n_words=8)` — matplotlib bar charts of top words per topic.

## src.language_models.summarizer

### `Summarizer(method="extractive", model="sshleifer/distilbart-cnn-12-6")`
- `summarize(text, n_sentences=3, max_length=130, min_length=30) -> str`
- `extractive(text, n_sentences=3) -> str` — static; TF-IDF sentence ranking.
- `_abstractive(...)` — lazy-loads transformers only when `method="abstractive"`.

## src.language_models.embeddings

### `SemanticSearch(backend="tfidf", model="sentence-transformers/all-MiniLM-L6-v2")`
- `index(documents) -> self`
- `search(query, k=5) -> list[dict]` — each `{index, score, snippet, category?}`.

## src.language_models.generator

### `ContentGenerator()`
- `enhance(analysis) -> str` — narrative brief from an analysis dict.
- `expand_query(query, per_word=2) -> str` — static; WordNet synonym expansion.

## src.multilingual

### `LanguageDetector()`
- `detect(text) -> str` — ISO language code.

### `Translator(target="en")`
- `translate(text, target=None) -> str`

### `CrossLingualAnalyzer(translator=None, detector=None)`
- `to_english(text) -> dict` — `{detected_language, translated_text}`.

## src.conversation

### `IntentClassifier()`
- `classify(query) -> str` — one of classify, sentiment, entities, summarize,
  search, topics.

### `QueryProcessor(bot=None, summarizer=None, search=None, topic_modeler=None)`
- `process(query, article=None) -> dict` — routes by detected intent.

### `ResponseGenerator()`
- `format(intent, result) -> str` — natural-language response.

## src.data_processing

### `TextPreprocessor(min_token_len=2)`
- `preprocess(text) -> str`, `transform(texts) -> list[str]`

### `FeatureExtractor(max_features=5000, ngram_range=(1,2), min_df=5, max_df=0.9)`
- `fit_transform(documents)`, `transform(documents)`, `feature_names()`,
  `top_terms(X, labels, category, n=12)`

### `DataValidator(text_col="text", category_col="category", min_words=5)`
- `validate(df) -> dict`, `clean(df) -> pd.DataFrame`

## src.utils
- `evaluation.evaluate(y_true, y_pred) -> dict`
- `export.save_json(obj, path)`, `export.dict_to_markdown(d, title)`
- `visualization.plot_confusion(...)`, `visualization.plot_class_balance(...)`
