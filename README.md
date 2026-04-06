# Currency Converter Web App

A modern currency converter built with Streamlit and live exchange rates.

## Features

- Real-time rates from ExchangeRate API
- Convert between major global currencies
- Precision up to 6 decimal places
- Clean blue-themed UI
- One-click deploy on Streamlit Community Cloud

## Tech Stack

- Python
- Streamlit
- Requests

## Project Structure

```text
currency-converter-app/
|- app.py
|- requirements.txt
|- .gitignore
|- README.md
```

## Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/AtreyoH/Currency-Converter.git
   cd Currency-Converter
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run app.py
   ```
4. Open the local URL shown in terminal (usually `http://localhost:8501`).

## Deploy on Streamlit Community Cloud

1. Push your latest code to GitHub.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app**.
4. Select:
   - Repository: `AtreyoH/Currency-Converter`
   - Branch: `main`
   - Main file path: `app.py`
5. In Advanced settings:
   - Python version: `3.11` (recommended)
   - Secrets: leave empty (not required for this app)
6. Click **Deploy**.

After deployment, Streamlit gives you a public URL you can share.

## Troubleshooting

- If deployment fails, check app logs in Streamlit Cloud.
- If API call fails temporarily, refresh the app after a few seconds.
- If dependencies fail to install, redeploy after confirming `requirements.txt` is committed.