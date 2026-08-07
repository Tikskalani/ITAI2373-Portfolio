# NewsBot 2.0 — Deployment Guide

## Local (development)

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py            # http://localhost:5000, debug on
```

## Local (production server)

Use a WSGI server rather than Flask's dev server:

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:8000 app:app
```

The app trains its models once at startup from `data/raw/newsbot_bbc.csv`, so the
first request after boot is fast. Two workers is plenty for demo traffic.

## Render (free tier, recommended for a public demo link)

1. Push the repo to GitHub (already done).
2. Create a new Web Service on Render, point it at the repo, root
   `ITAI2373-NewsBot-Final/`.
3. Build command:
   `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
4. Start command: `gunicorn app:app`
5. Deploy. Render gives you a public `https://<name>.onrender.com` URL.

## Heroku

Add a `Procfile` with `web: gunicorn app:app`, then:

```bash
heroku create
git subtree push --prefix ITAI2373-NewsBot-Final heroku main
```

## Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && python -m spacy download en_core_web_sm
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
```

```bash
docker build -t newsbot2 .
docker run -p 8000:8000 newsbot2
```

## Notes

- Keep transformer extras out of the deploy unless you need them; they add a large
  image and long cold starts. The defaults (TF-IDF search, extractive summaries)
  are enough for the demo.
- Never commit real API keys. `config/api_keys_template.txt` shows the format.
