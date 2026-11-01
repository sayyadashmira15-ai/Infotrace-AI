from fastapi.responses import FileResponse
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.extractor import extract_website
from backend.analyzer import analyze_sources

app = FastAPI(
    title="InfoTrace AI",
    description="AI-powered Information Gap Detection Platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WebsiteRequest(BaseModel):
    url: str

class AnalysisRequest(BaseModel):
    sources: list[dict]

@app.get("/")
def home():
    return {
        "message": "Welcome to InfoTrace AI!",
        "status": "Backend is running"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/extract")
def extract(request: WebsiteRequest):
    return extract_website(request.url)

@app.post("/analyze")
def analyze(request: AnalysisRequest):
    return analyze_sources(request.sources)
@app.get("/dashboard")
def dashboard():
    html_path = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
    return FileResponse(html_path)