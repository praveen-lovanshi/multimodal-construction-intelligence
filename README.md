# Multimodal Construction Intelligence Platform

**Skill Wallet Capstone Project 1**

An AI-assisted Streamlit decision-support application for construction safety, crack diagnostics, project planning, INR valuation, and weather-aware site coordination.

## Features

- **Site Safety & PPE Audit:** Upload a construction image and receive a safety score, PPE checklist, hazards, severity levels, and corrective remedies.
- **Crack Diagnostics:** Upload a concrete or wall image and receive a defect type, estimated width, causes, risks, recommended repairs, and urgency.
- **Planning & Valuation:** Calculate indicative project budget, incurred capex, material quantities, price per square foot, and market valuation in Indian Rupees.
- **Daily Site Assistant:** Ask construction engineering questions with site-condition context.
- **Weather Advisory:** Receive GO, NO-GO, or GO-with-controls guidance for different weather conditions.
- **Reports:** Download structured safety, crack, and planning outputs as JSON.
- **Dashboard UI:** Industrial dark theme, orange construction accents, status cards, module cards, and workspace navigation.

## AI and Demo Mode

The application supports two modes:

1. **Demo Mode:** works without an API key and is suitable for student demonstrations and free deployment.
2. **Gemini Mode:** optionally analyzes text and uploaded images using a Google Gemini API key.

Enter a key in the sidebar for local testing. On Streamlit Cloud, add it under **App settings → Secrets**. Never commit API keys.

## Technology Stack

- Python 3.11 or 3.12 recommended
- Streamlit
- Google Generative AI SDK
- Custom CSS dashboard design
- JSON-based outputs
- No database required
- Compatible with free Streamlit Community Cloud deployment

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── config.toml
└── README.md
```

## Run Locally

```powershell
cd "C:\Users\Guest1\Desktop\New folder1223"
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

The `pip install` command is normally needed only during first setup, after cloning the project, or after changing `requirements.txt`. It does not need to be run every time.

## Free Streamlit Community Cloud Deployment

1. Create a public GitHub repository.
2. Push this project to the repository.
3. Open [Streamlit Community Cloud](https://share.streamlit.io/).
4. Choose **Create app**.
5. Select the repository, branch `main`, and main file `app.py`.
6. Click **Deploy**.

The app works without a Gemini key in Demo Mode. If you later receive a free Gemini key, add this under **App settings → Secrets**:

```toml
GEMINI_API_KEY = "your-key"
```

## GitHub Commands

The local Git repository is already initialized in this project folder. Create an empty public repository on GitHub first, then run:

```powershell
cd "C:\Users\Guest1\Desktop\New folder1223"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPOSITORY` with your GitHub details.

For future changes:

```powershell
git add .
git commit -m "Describe your change"
git push
```

Check the repository before pushing:

```powershell
git status
```

## Security

Do not commit Gemini API keys, `.env` files, `.streamlit/secrets.toml`, private construction images, or confidential site documents. These files are excluded by [.gitignore](./.gitignore).

## Limitations

This application provides indicative decision support. It does not replace a licensed structural engineer, safety professional, quantity surveyor, valuation professional, or local authority review.

Image-based crack widths, safety scores, costs, and valuations must be verified using professional inspection, measurements, current local rates, engineering drawings, and applicable regulations.

## Project Status

- Streamlit dashboard implemented
- Demo mode implemented
- Optional Gemini multimodal integration implemented
- Dark dashboard UI implemented
- Safety, crack, planning, valuation, assistant, and weather workspaces implemented
- JSON report downloads implemented
- Local startup validated
- Ready for GitHub and Streamlit Community Cloud deployment
