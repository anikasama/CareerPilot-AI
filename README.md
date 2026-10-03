# CareerPilot AI

CareerPilot AI is an AI-powered career intelligence platform that analyzes resumes against target job descriptions.

## Core Features

- PDF Resume Upload
- Resume Text Extraction
- ATS Resume Analysis
- Technical Skill Detection
- Job Description Skill Detection
- Job Match Score
- Matched Skills
- Missing Skills
- Placement Readiness
- Personalized Skill Roadmap
- Practical Project Recommendations
- AI Career Feedback
- Interview Questions
- Responsive Dashboard

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- FastAPI
- Python
- PyMuPDF
- OpenAI Responses API

## Project Structure

CareerPilot-AI/

backend/
  app/
    routes/
    services/
    utils/

frontend/
  src/
    components/
    pages/
    services/

## Main User Flow

Upload Resume
        ↓
Paste Job Description
        ↓
CareerPilot AI Analysis
        ↓
ATS Score
        ↓
Job Match
        ↓
Skill Gap
        ↓
Placement Readiness
        ↓
Career Roadmap
        ↓
AI Career Feedback
        ↓
Interview Preparation

## Backend

The main API endpoint is:

POST /api/analyze

It accepts:

- file: PDF resume
- job_description: target job description

## AI Feedback

If OPENAI_API_KEY is configured, CareerPilot AI uses the OpenAI Responses API for personalized career feedback.

If no API key is configured, the application automatically uses its built-in rule-based career feedback system.

## Environment Variables

Backend `.env`:

OPENAI_API_KEY=
OPENAI_MODEL=gpt-6-luna
FRONTEND_ORIGINS=http://localhost:5173
MAX_UPLOAD_MB=5

## Important

CareerPilot ATS scoring is a transparent rule-based prototype. It should not be represented as an official ATS used by a specific company or as a scientifically validated hiring predictor.

The application currently processes text-based PDF resumes. Image-only/scanned PDFs may require OCR in a future version.

## Production

Before deployment:

1. Install backend dependencies.
2. Install frontend dependencies.
3. Configure environment variables.
4. Test the `/health` endpoint.
5. Run the frontend build.
6. Test resume analysis.
7. Deploy backend and frontend separately or behind the same domain.
8. Update FRONTEND_ORIGINS to the production frontend URL.
9. Configure OPENAI_API_KEY if AI feedback is required.