# EcoTrack — Carbon Footprint Tracker

A Streamlit application that estimates a monthly personal carbon footprint from home energy, transport, diet and household waste inputs. It displays category totals, practical reduction ideas, session history and CSV export.

## Features
- Monthly activity input form
- Estimated total and annualized CO₂e
- Category-wise emissions chart
- Personalized reduction suggestions
- Session history and CSV download
- No API key, database or hardware required

## Requirements
Python 3.10–3.12 recommended, VS Code, and internet for first-time package installation.

## Run on Windows PowerShell
Open this folder in VS Code, then run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If `py -3.12` is unavailable, install Python 3.12 and enable **Add Python to PATH**. Alternatively use `python -m venv .venv` if your Python version is 3.10–3.12.

If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Streamlit normally opens `http://localhost:8501`.

## Calculation limitations
The bundled factors are simplified illustrative teaching values, not official or location-specific factors. Results are estimates, not verified carbon accounting. For research or public reporting, replace them with documented factors appropriate to the geography, year and system boundary. Apportion shared household energy fairly.

## GitHub
Create an empty repository named `EcoTrack-Carbon-Footprint-Tracker`, then run:
```powershell
git init
git add .
git commit -m "Initial commit - EcoTrack Carbon Footprint Tracker"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/EcoTrack-Carbon-Footprint-Tracker.git
git push -u origin main
```
