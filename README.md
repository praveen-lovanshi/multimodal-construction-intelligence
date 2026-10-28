# Multimodal Construction Intelligence Platform

Skill Wallet Capstone Project 1: an AI-assisted Streamlit application for construction safety, crack diagnostics, planning, INR valuation, and weather-aware site assistance.

Python 3.11 or 3.12 is recommended for the smoothest local setup. The app does not require Pillow; uploaded image bytes are sent directly to Gemini.

## Features

- Site safety and PPE audit from JPG/PNG images.
- Crack type, width, severity, causes, repair, and urgency assessment.
- Construction budget, incurred capex, material quantities, and indicative property valuation in INR.
- Weather-aware GO / NO-GO guidance and a construction assistant chat.
- Structured JSON reports with download buttons.
- Demonstration mode works without an API key; Gemini adds multimodal reasoning when configured.

## Run locally

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the URL printed by Streamlit, normally `http://localhost:8501`. In the sidebar, optionally enter a Google Gemini API key. Never commit API keys.

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Select the repository, branch, and `app.py` as the main file.
4. In **Advanced settings → Secrets**, add:

```toml
GEMINI_API_KEY = "your-key"
```

The current app also accepts a key entered in the sidebar. For a production deployment, prefer the secret and update `ask_gemini` to read `st.secrets["GEMINI_API_KEY"]`.

## Push to GitHub

```powershell
git init
git add .
git commit -m "Build multimodal construction intelligence platform"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repository>.git
git push -u origin main
```

If the remote repository already exists, skip `git init` and use the existing remote. Confirm `.env` and `.streamlit/secrets.toml` are ignored before pushing.

## Important limitation

Outputs are indicative decision support, not a substitute for a licensed structural engineer, safety professional, quantity surveyor, or local authority requirements. Image-based crack width and safety status must be verified on site.
