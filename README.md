# StatBuddy — Streamlit app (Gemini)

A Streamlit version of your SPSS Statistical Test Selector chatbot, configured to use the Google Gemini API.

## 1. Requirements

- Python 3.9 or newer
- A Google Gemini API key

## 2. Install

Unzip the package, open Terminal in the `StatBuddy_Streamlit` folder, then run:

```bash
python3 -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\\Scripts\\Activate.ps1

python -m pip install -r requirements.txt
```

## 3. Configure your Gemini API key

Open `.streamlit/secrets.toml` and replace the placeholder with your own key:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

Get a Gemini API key from https://aistudio.google.com/app/apikey. Keep this file private; do not upload it to GitHub or share it. The included `.gitignore` excludes it from Git.

## 4. Run the app

```bash
streamlit run app.py
```

Streamlit will open StatBuddy in your browser. The app uses the `gemini-2.5-flash` model. Your chatbot manual and tutoring instructions are embedded in `app.py`. Conversation history is stored in Streamlit session state and limited to the last 12 messages. Use **Clear chat** in the sidebar to reset the conversation.
