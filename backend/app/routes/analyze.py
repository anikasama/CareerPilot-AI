import os

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.services.career_report import generate_career_report
from app.utils.resume_parser import extract_text_from_pdf


router = APIRouter(prefix="/api", tags=["Analysis"])

MAX_UPLOAD_MB = float(
    os.getenv("MAX_UPLOAD_MB", "5")
)

MAX_UPLOAD_BYTES = int(
    MAX_UPLOAD_MB * 1024 * 1024
)


@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please select a resume PDF.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF resume files are supported.",
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Please provide a job description.",
        )

    if len(job_description.strip()) < 30:
        raise HTTPException(
            status_code=400,
            detail="Please provide a more detailed job description.",
        )

    try:
        file_bytes = await file.read()

        if len(file_bytes) > MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=413,
                detail=(
                    f"Resume file is too large. "
                    f"Maximum size is {MAX_UPLOAD_MB:g} MB."
                ),
            )

        parsed_resume = extract_text_from_pdf(file_bytes)

        report = generate_career_report(
            resume_text=parsed_resume["text"],
            job_description=job_description.strip(),
            filename=file.filename,
            pages=parsed_resume["pages"],
            words=parsed_resume["words"],
        )

        return report

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "CareerPilot AI could not analyze the resume. "
                "Please try again."
            ),
        ) from exc