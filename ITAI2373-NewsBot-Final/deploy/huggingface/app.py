"""
NewsBot Intelligence System 2.0 — Hugging Face Spaces (Gradio) front end.

This Space is self-contained: on first boot it clones the project repository,
puts the NewsBot package on the path, loads the BBC dataset, and trains the
lightweight components once. Everything after that runs in memory.

Files this Space needs (all in this folder): app.py, requirements.txt, README.md
"""
import os, sys, subprocess, importlib

REPO_URL = "https://github.com/Tikskalani/ITAI2373-Portfolio.git"
SUBDIR = "ITAI2373-NewsBot-Final"

def _ensure_code():
    # Already importable (e.g. local run)?
    for cand in (".", SUBDIR, os.path.join("ITAI2373-Portfolio", SUBDIR)):
        if os.path.isfile(os.path.join(cand, "src", "newsbot.py")):
            return os.path.abspath(cand)
    # Clone on a fresh Space
    if not os.path.isdir("ITAI2373-Portfolio"):
        subprocess.run(["git", "clone", "--depth", "1", REPO_URL], check=True)
    return os.path.abspath(os.path.join("ITAI2373-Portfolio", SUBDIR))

ROOT = _ensure_code()
sys.path.insert(0, ROOT)

# spaCy English model (installed via requirements wheel; fall back to download)
try:
    import spacy; spacy.load("en_core_web_sm")
except Exception:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=False)

import pandas as pd
import gradio as gr
from src.newsbot import NewsBot
from src.language_models.summarizer import Summarizer
from src.language_models.embeddings import SemanticSearch
from src.analysis.topic_modeler import TopicModeler
from src.conversation.query_processor import QueryProcessor

DF = pd.read_csv(os.path.join(ROOT, "data", "raw", "newsbot_bbc.csv"))
BOT = NewsBot(use_domain_rules=True).train(DF["text"], DF["category"])
SUMM = Summarizer(method="extractive")
SEARCH = SemanticSearch(backend="tfidf").index(DF["text"])
TM = TopicModeler(n_topics=5, method="lda"); TM.fit_transform(DF["text"])
QP = QueryProcessor(bot=BOT, summarizer=SUMM, search=SEARCH, topic_modeler=TM)


def analyze(text):
    text = (text or "").strip()
    if not text:
        return "Paste an article above, then press Analyze."
    a = BOT.analyze(text)
    c = a["classification"]; s = a["sentiment"]
    cat = c.get("category", "uncertain")
    conf = c.get("confidence")
    conf_s = f"{conf:.0%}" if isinstance(conf, (int, float)) else "n/a"
    ents = a.get("entities") or []
    ent_s = ", ".join(f"{e[0]} ({e[1]})" for e in ents) or "none found"
    terms = ", ".join(c.get("key_terms", [])[:6]) or "n/a"
    summary = SUMM.summarize(text, n_sentences=2)
    note = c.get("note", "")
    md = [f"### Category: **{cat}**  ·  confidence {conf_s}"]
    if note: md.append(f"> {note}")
    md += [
        f"**Sentiment:** {s.get('label','?')} (compound {s.get('compound',0):.2f})   ·   "
        f"**Emotion:** {s.get('emotion','?')}",
        f"**Entities:** {ent_s}",
        f"**Key terms:** {terms}",
        f"**Summary:** {summary}",
    ]
    return "\n\n".join(md)

def ask(question, article):
    question = (question or "").strip()
    if not question:
        return "Type a question, for example: what is the sentiment?"
    try:
        res = QP.process(question, (article or "").strip() or None)
        ans = res.get("response", res) if isinstance(res, dict) else res
        return f"**Answer:** {ans}"
    except Exception as e:
        return f"Could not answer that ({type(e).__name__})."

def find_similar(query):
    query = (query or "").strip()
    if not query:
        return "Type a phrase, for example: football championship final."
    rows = ["| Category | Score | Snippet |", "|---|---|---|"]
    for i, score, snippet in SEARCH.search(query, k=5):
        cat = DF["category"].iloc[i]
        rows.append(f"| {cat} | {score:.3f} | {snippet[:90].strip()}... |")
    return "\n".join(rows)

def topics_md():
    rows = ["Topics discovered by LDA with no labels (they line up with the five news beats):",
            "", "| Topic | Top words |", "|---|---|"]
    for tid, words in TM.get_all_topics(n_words=7).items():
        rows.append(f"| Topic {tid} | {', '.join(words)} |")
    return "\n".join(rows)

EXAMPLE = ("A major technology company launched a powerful new artificial intelligence "
           "system, but said it would limit access to a small group of trusted partners "
           "at first, intensifying competition between computing firms.")

with gr.Blocks(title="NewsBot Intelligence System 2.0", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        "# NewsBot Intelligence System 2.0\n"
        "Advanced NLP news analysis · ITAI 2373 Final Project · Trilok Kalani  \n"
        f"Trained on {len(DF)} BBC News articles across {DF['category'].nunique()} categories."
    )
    with gr.Tab("Analyze an article"):
        inp = gr.Textbox(label="Article text", lines=6, placeholder="Paste a news article here...")
        gr.Examples([[EXAMPLE]], inputs=[inp])
        out = gr.Markdown()
        gr.Button("Analyze", variant="primary").click(analyze, inp, out)
    with gr.Tab("Ask NewsBot"):
        gr.Markdown("Ask about the article you paste below. Try: what is the sentiment, "
                    "who is mentioned, give me a summary, what topics are there.")
        art = gr.Textbox(label="Article (context for the question)", lines=4, value=EXAMPLE)
        q = gr.Textbox(label="Your question", placeholder="what is the sentiment?")
        aout = gr.Markdown()
        gr.Button("Ask", variant="primary").click(ask, [q, art], aout)
    with gr.Tab("Find similar articles"):
        sq = gr.Textbox(label="Search phrase", placeholder="football championship final")
        sout = gr.Markdown()
        gr.Button("Search", variant="primary").click(find_similar, sq, sout)
    with gr.Tab("Topics"):
        gr.Markdown(topics_md())

if __name__ == "__main__":
    demo.launch()
