import os

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.ats_engine import calculate_ats_score
from app.utils.resume_parser import extract_text_from_pdf


router = APIRouter(prefix="/api", tags=["Resume"])

MAX_UPLOAD_MB = float(
    os.getenv("MAX_UPLOAD_MB", "5")
)

MAX_UPLOAD_BYTES = int(
    MAX_UPLOAD_MB * 1024 * 1024
)


@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please select a resume PDF.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    try:
        file_bytes = await file.read()

        if len(file_bytes) > MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=413,
                detail=(
                    f"Maximum resume size is "
                    f"{MAX_UPLOAD_MB:g} MB."
                ),
            )

        parsed = extract_text_from_pdf(file_bytes)
        ats = calculate_ats_score(parsed["text"])

        return {
            "filename": file.filename,
            "pages": parsed["pages"],
            "words": parsed["words"],
            "ats": ats,
        }

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
            detail="Resume processing failed.",
        ) from exc