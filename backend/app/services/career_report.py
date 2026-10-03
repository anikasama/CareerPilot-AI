from app.services.ai_feedback import generate_ai_feedback
from app.services.ats_engine import calculate_ats_score
from app.services.job_matcher import match_resume_with_job
from app.services.roadmap import build_roadmap


def calculate_placement_readiness(
    ats_score: int,
    job_match: int,
    skill_coverage: int,
) -> dict:
    ats_weight = ats_score * 0.40
    job_weight = job_match * 0.40
    skill_weight = skill_coverage * 0.20

    overall = round(
        ats_weight
        + job_weight
        + skill_weight
    )

    if overall >= 85:
        status = "Excellent"
        rating = "★★★★★"
    elif overall >= 70:
        status = "Strong"
        rating = "★★★★☆"
    elif overall >= 55:
        status = "Developing"
        rating = "★★★☆☆"
    else:
        status = "Needs Improvement"
        rating = "★★☆☆☆"

    return {
        "overall_readiness": overall,
        "status": status,
        "rating": rating,
        "ats_score": ats_score,
        "job_match": job_match,
        "skill_coverage": skill_coverage,
        "breakdown": {
            "ats_weight": round(ats_weight),
            "job_match_weight": round(job_weight),
            "skill_coverage_weight": round(skill_weight),
        },
    }


def generate_career_report(
    resume_text: str,
    job_description: str,
    filename: str = "resume.pdf",
    pages: int = 1,
    words: int = 0,
) -> dict:
    ats = calculate_ats_score(resume_text)

    job_match = match_resume_with_job(
        resume_text,
        job_description,
    )

    roadmap = build_roadmap(
        job_match["missing_skills"]
    )

    placement = calculate_placement_readiness(
        ats_score=ats["score"],
        job_match=job_match["score"],
        skill_coverage=job_match["skill_coverage"],
    )

    ai_feedback = generate_ai_feedback(
        resume_text=resume_text,
        job_description=job_description,
        ats_score=ats["score"],
        job_match=job_match["score"],
        matched_skills=job_match["matched_skills"],
        missing_skills=job_match["missing_skills"],
    )

    return {
        "resume": {
            "filename": filename,
            "pages": pages,
            "words": words,
        },
        "ats": ats,
        "job_match": job_match,
        "roadmap": roadmap,
        "placement": placement,
        "ai_feedback": ai_feedback,
    }