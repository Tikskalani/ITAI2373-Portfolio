# Deploy to Render (backup path)

Copy `Procfile` and `runtime.txt` into the `ITAI2373-NewsBot-Final/` folder,
then on render.com: New > Web Service > connect this GitHub repo, set root
directory to `ITAI2373-NewsBot-Final`, build
`pip install -r requirements.txt && python -m spacy download en_core_web_sm`,
start `gunicorn app:app`. Free tier gives a public onrender.com URL (cold starts
slowly because the models train at boot).
