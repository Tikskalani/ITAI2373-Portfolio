"""NewsBot 2.0 Flask web application (bonus frontend).

Run:  python app.py    then open http://localhost:5000
The NLP components are trained once at startup on the bundled BBC dataset.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from flask import Flask, render_template, request, jsonify

from src.newsbot import NewsBot
from src.analysis.topic_modeler import TopicModeler
from src.language_models.summarizer import Summarizer
from src.language_models.embeddings import SemanticSearch
from src.conversation.query_processor import QueryProcessor
from src.data_processing.text_preprocessor import TextPreprocessor

app = Flask(__name__)

# ---- load & train the NLP stack once at startup ----------------------------
DATA = os.path.join(os.path.dirname(__file__), "data", "raw", "newsbot_bbc.csv")
_df = pd.read_csv(DATA)
_pre = TextPreprocessor()

bot = NewsBot().train(_df["text"], _df["category"])
summarizer = Summarizer(method="extractive")
search = SemanticSearch(backend="tfidf").index(_df["text"])
topic_modeler = TopicModeler(n_topics=5, method="lda")
topic_modeler.fit_transform(_pre.transform(_df["text"]))
qp = QueryProcessor(bot=bot, summarizer=summarizer, search=search, topic_modeler=topic_modeler)
CATEGORIES = sorted(_df["category"].unique())


@app.route("/")
def dashboard():
    return render_template("dashboard.html", categories=CATEGORIES, n_articles=len(_df))


@app.route("/analyze", methods=["POST"])
def analyze():
    text = (request.get_json(silent=True) or {}).get("text", "")
    if not text.strip():
        return jsonify({"error": "Please provide article text."}), 400
    r = bot.analyze(text)
    return jsonify({
        "classification": r["classification"],
        "sentiment": r["sentiment"],
        "entities": r["entities"],
        "summary": summarizer.summarize(text, n_sentences=3),
    })


@app.route("/query", methods=["POST"])
def query():
    data = request.get_json(silent=True) or {}
    q = data.get("query", "")
    article = data.get("article") or None
    if not q.strip():
        return jsonify({"error": "Please provide a query."}), 400
    return jsonify(qp.process(q, article=article))


@app.route("/similar", methods=["POST"])
def similar():
    q = (request.get_json(silent=True) or {}).get("query", "")
    hits = search.search(q, k=5)
    return jsonify({"results": [
        {"score": s, "snippet": snip, "category": str(_df["category"].iloc[i])} for i, s, snip in hits]})


@app.route("/topics")
def topics():
    return jsonify(topic_modeler.get_all_topics(8))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
