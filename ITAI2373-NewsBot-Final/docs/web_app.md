# NewsBot 2.0 Web Application

A Flask frontend for the NewsBot pipeline.

## Run locally
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py
# open http://localhost:5000
```

## Endpoints
- `GET  /`         dashboard UI
- `POST /analyze`  body `{"text": "..."}` -> classification, sentiment, entities, summary
- `POST /query`    body `{"query": "...", "article": "..."}` -> intent + natural-language response
- `POST /similar`  body `{"query": "..."}` -> top similar articles
- `GET  /topics`   discovered LDA topics

## Deploy (options)
- **Render / Railway / Heroku:** add a `Procfile` with `web: gunicorn app:app` and `gunicorn` to requirements.
- **Streamlit alternative:** the same `src/` modules can back a Streamlit app for rapid prototyping.
