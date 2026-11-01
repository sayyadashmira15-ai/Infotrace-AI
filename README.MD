# InfoTrace AI

**AI-Powered Research Intelligence & Verification Platform**

InfoTrace AI helps users analyze website content, identify missing information, detect potentially outdated information, and assess research confidence and risk using AI.

## Features

- **Information Gap Radar:** Identifies missing or incomplete information.
- **Truth Clash Detector:** Detects potentially conflicting claims.
- **Information Expiry Tracker:** Flags potentially outdated information.
- **Evidence Confidence Score:** Estimates confidence based on available evidence.
- **Smart Verification Agent:** Generates a verification checklist.
- **Missing Connection Finder:** Identifies potentially relevant relationships.
- **Research Risk Report:** Provides an overall research risk assessment.

## Tech Stack

- Python
- FastAPI
- HTML, CSS, JavaScript
- Groq AI API
- BeautifulSoup
- Requests

## Project Structure

```text
INFOTrash AI/
├── backend/
│   ├── main.py
│   ├── extractor.py
│   └── analyzer.py
├── frontend/
│   └── index.html
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd "INFOTrash AI"
```

### 2. Create and activate virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```


### 5. Start the application

```bash
python -m uvicorn backend.main:app --reload
```

### 6. Open the dashboard

```text
http://127.0.0.1:8000/dashboard
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Backend welcome |
| `/health` | GET | Health check |
| `/dashboard` | GET | Web dashboard |
| `/extract` | POST | Extract website content |
| `/analyze` | POST | Analyze research sources |

## How It Works

1. User submits a website URL.
2. Backend extracts readable website content.
3. Groq AI analyzes the supplied content.
4. The platform identifies research gaps, outdated information, possible conflicts, and missing connections.
5. Results are displayed on the dashboard.

## Important Note

AI-generated findings are preliminary and should be independently verified using reliable sources. Confidence and risk scores are estimates, not guarantees of factual accuracy.

## Project

Developed for **SHINCHAN ONLINE HACKATHON 2026**.
