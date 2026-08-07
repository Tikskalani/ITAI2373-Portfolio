# Deployment Instructions (quick reference)

Local demo:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py     # http://localhost:5000
```

Public URL (Render free tier):
- Build: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
- Start: `gunicorn app:app`

Full options (Heroku, Docker, gunicorn tuning) are in `deployment_guide.md`.
