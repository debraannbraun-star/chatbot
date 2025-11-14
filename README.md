# UbiMinds AI Adoption Challenge — Chatbot

This repository contains a Streamlit-based assessment chatbot used in the UbiMinds AI Adoption Challenge.

Quick start (local)
1. Create and activate a Python environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the app:

```bash
streamlit run streamlit_app.py
```

3. Open the URL printed by Streamlit (typically `http://localhost:8501`).

Deploy to Streamlit Community Cloud
1. Push this repo to GitHub (this repo already includes a remote named `origin`).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click "New app", choose this repository, branch `main`, and set the app file to `streamlit_app.py`.
4. Streamlit will install dependencies from `requirements.txt` and deploy. You will get a public URL to share.
5. Add your OpenAI API key:
   - After the app deploys, click the **⋮** (menu) in the top right → **Settings** → **Secrets**.
   - Paste: `openai_api_key = "sk-...your-actual-key..."`
   - Click **Save**. Streamlit will automatically restart the app with the secret.

Running locally with OpenAI
- Export the API key before running:
  ```bash
  export OPENAI_API_KEY="sk-...your-actual-key..."
  streamlit run streamlit_app.py
  ```
- Or edit `.streamlit/secrets.toml` and uncomment the key line (not committed to Git).

Notes
- Do not commit API keys or secrets. Use Streamlit Secrets or environment variables for keys (e.g., `OPENAI_API_KEY`).
- `.streamlit/secrets.toml` is in `.gitignore` and will never be committed.
- `requirements.txt` lists `streamlit` and `openai` which are needed for this app.
