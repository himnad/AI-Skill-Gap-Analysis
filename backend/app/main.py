import os
import tempfile

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.services.analysis_service import analyze_resume_and_job


app = FastAPI(
    title="AI Driven Skill Gap Analysis API",
    version="1.0.0",
)


# Allow the frontend to communicate with the backend.
# Localhost origins are used during development.
# FRONTEND_URL will be added when the frontend is deployed.
frontend_url = os.environ.get("FRONTEND_URL", "").rstrip("/")

allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

if frontend_url:
    allowed_origins.append(frontend_url)


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI Driven Skill Gap Analysis API",
    }


@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...),
):
    """
    Upload a resume and job description PDF and
    return skill gaps and NPTEL recommendations.
    """

    # Create a temporary file for the uploaded resume.
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf",
    ) as resume_file:
        resume_file.write(await resume.read())
        resume_path = resume_file.name

    # Create a temporary file for the uploaded job description.
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf",
    ) as jd_file:
        jd_file.write(await job_description.read())
        jd_path = jd_file.name

    try:
        # Run the complete AI skill-gap analysis pipeline.
        result = analyze_resume_and_job(
            resume_path,
            jd_path,
        )

        return result

    finally:
        # Delete temporary uploaded files after processing.
        if os.path.exists(resume_path):
            os.remove(resume_path)

        if os.path.exists(jd_path):
            os.remove(jd_path)