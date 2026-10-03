from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.ai_feedback import generate_ai_feedback


router = APIRouter(prefix="/api", tags=["AI"])


class AIFeedbackRequest(BaseModel):
    resume_text: str = Field(..., min_length=50)
    job_description: str = Field(..., min_length=30)
    ats_score: int = Field(..., ge=0, le=100)
    job_match: int = Field(..., ge=0, le=100)
    matched_skills: list[str] = []
    missing_skills: list[str] = []


@router.post("/ai-feedback")
def ai_feedback(request: AIFeedbackRequest):
    return generate_ai_feedback(
        resume_text=request.resume_text,
        job_description=request.job_description,
        ats_score=request.ats_score,
        job_match=request.job_match,
        matched_skills=request.matched_skills,
        missing_skills=request.missing_skills,
    )