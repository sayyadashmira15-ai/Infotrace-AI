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

## Example Usage

### Example: Analyzing WHO Health Topics

**Input URL:**

https://www.who.int/health-topics

**Steps:**
1. Open the InfoTrace AI dashboard.
2. Paste the WHO health topics URL.
3. Click the Extract button to collect website content.
4. Click Run Analysis to start AI-powered research analysis.

**Example Analysis Output:**

| Research Module | Example Result |
|---|---|
| Information Gap Radar | 5 information gaps identified |
| Truth Clash Detector | No conflicting claims detected |
| Information Expiry Tracker | 1 potentially outdated item |
| Evidence Confidence Score | 20% |
| Smart Verification Agent | 4 verification actions |
| Missing Connection Finder | 3 possible connections |
| Research Risk Report | Medium risk (45/100) |

**Note:** These are example results from one test run, not guaranteed outputs. Actual results may vary depending on the website content and AI analysis.

## Project

Developed for **SHINCHAN ONLINE HACKATHON 2026**.
