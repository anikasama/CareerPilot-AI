import json
import os
import re

from app.services.job_matcher import detect_skills


def fallback_feedback(
    resume_text: str,
    job_description: str,
    ats_score: int,
    job_match: int,
    matched_skills: list[str],
    missing_skills: list[str],
) -> dict:
    strengths = []

    if ats_score >= 80:
        strengths.append("Your resume has a strong overall ATS structure.")
    elif ats_score >= 60:
        strengths.append("Your resume has a reasonable ATS foundation.")
    else:
        strengths.append(
            "Your resume has a foundation, but several ATS areas need improvement."
        )

    if matched_skills:
        strengths.append(
            f"You already match {len(matched_skills)} recognized job skill(s)."
        )

    if "Projects" in resume_text:
        strengths.append(
            "Your resume includes project-related content."
        )

    weaknesses = []

    if ats_score < 75:
        weaknesses.append(
            "The resume can be improved for structure, relevance and measurable impact."
        )

    if job_match < 60:
        weaknesses.append(
            "The resume currently covers only part of the recognized job requirements."
        )

    if missing_skills:
        weaknesses.append(
            "Some important technical skills from the job description are missing."
        )

    if not weaknesses:
        weaknesses.append(
            "Continue improving measurable results and role-specific keywords."
        )

    suggestions = [
        "Tailor the Skills and Projects sections to the target role.",
        "Use action verbs and quantify project or internship outcomes.",
        "Keep the most relevant technologies visible near the top of the resume.",
    ]

    if missing_skills:
        suggestions.append(
            "Prioritize learning: "
            + ", ".join(missing_skills[:5])
            + "."
        )

    interview_questions = [
        "Walk me through your most relevant project.",
        "Which technical skill in this job description are you strongest in?",
        "Describe a difficult technical problem you solved.",
        "How do you test and debug your code?",
        "What skill are you currently improving and why?",
    ]

    if missing_skills:
        interview_questions[4] = (
            f"How would you approach learning and applying {missing_skills[0]}?"
        )

    score = round(
        min(
            100,
            max(
                0,
                ats_score * 0.45
                + job_match * 0.45
                + min(len(matched_skills) * 2, 10),
            ),
        )
    )

    return {
        "score": score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "interview_questions": interview_questions,
        "source": "CareerPilot AI rule-based fallback",
    }


def clean_json_text(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text, flags=re.IGNORECASE)
        text = re.sub(r"```$", "", text).strip()

    return text


def generate_ai_feedback(
    resume_text: str,
    job_description: str,
    ats_score: int,
    job_match: int,
    matched_skills: list[str],
    missing_skills: list[str],
) -> dict:
    fallback = fallback_feedback(
        resume_text=resume_text,
        job_description=job_description,
        ats_score=ats_score,
        job_match=job_match,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
    )

    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        return fallback

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        model = os.getenv(
            "OPENAI_MODEL",
            "gpt-6-luna",
        )

        prompt = f"""
You are CareerPilot AI, a professional career coach.

Analyze the candidate resume against the job description.

Return ONLY valid JSON with exactly these keys:

{{
  "score": number,
  "strengths": ["string"],
  "weaknesses": ["string"],
  "missing_skills": ["string"],
  "suggestions": ["string"],
  "interview_questions": ["string"]
}}

Rules:
- score must be 0 to 100.
- Use concise, practical career advice.
- Do not invent experience.
- Missing skills must come from the recognized missing skills list.
- Give 3 to 5 strengths.
- Give 3 to 5 weaknesses.
- Give 4 to 6 suggestions.
- Give 5 interview questions.
- Focus on placement readiness and the target job.

ATS Score: {ats_score}/100
Job Match: {job_match}%

Matched Skills:
{", ".join(matched_skills) if matched_skills else "None"}

Missing Skills:
{", ".join(missing_skills) if missing_skills else "None"}

RESUME:
{resume_text[:16000]}

JOB DESCRIPTION:
{job_description[:10000]}
"""

        response = client.responses.create(
            model=model,
            input=prompt,
        )

        raw_output = response.output_text
        parsed = json.loads(clean_json_text(raw_output))

        required_keys = {
            "score",
            "strengths",
            "weaknesses",
            "missing_skills",
            "suggestions",
            "interview_questions",
        }

        if not required_keys.issubset(parsed.keys()):
            return fallback

        parsed["score"] = max(
            0,
            min(100, int(parsed["score"])),
        )

        parsed["missing_skills"] = missing_skills
        parsed["source"] = "OpenAI"

        return parsed

    except Exception:
        return fallback