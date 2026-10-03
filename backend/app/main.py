import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.ai import router as ai_router
from app.routes.analyze import router as analyze_router
from app.routes.upload import router as upload_router

load_dotenv()

app = FastAPI(
    title="CareerPilot AI",
    description=(
        "AI-powered Resume Analyzer, Job Matcher, "
        "Skill Gap Detector, Career Roadmap and Placement Readiness Platform."
    ),
    version="2.0.0",
)

origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "name": "CareerPilot AI",
        "version": "2.0.0",
        "status": "running",
        "message": "CareerPilot AI backend is running successfully.",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "CareerPilot AI API",
    }


app.include_router(analyze_router)
app.include_router(upload_router)
app.include_router(ai_router)