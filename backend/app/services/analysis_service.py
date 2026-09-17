from app.services.gemini_service import (
    extract_missing_skills,
    extract_resume_skills,
)
from app.services.pdf_service import extract_text_from_pdf
from app.services.recommendation_service import recommend_courses


def analyze_resume_and_job(
    resume_path: str,
    job_description_path: str,
) -> dict:
    """
    Run the complete skill-gap analysis pipeline.
    """

    # 1. Extract text from both PDFs.
    resume_text = extract_text_from_pdf(resume_path)
    job_description_text = extract_text_from_pdf(
        job_description_path
    )

    # 2. Extract skills from the resume.
    resume_skills = extract_resume_skills(resume_text)

    # 3. Identify missing skills.
    missing_skills = extract_missing_skills(
        job_description_text,
        resume_skills,
    )

    # 4. Recommend NPTEL courses for the missing skills.
    recommendations = recommend_courses(
        missing_skills,
        top_k=5,
    )

    return {
        "resume_skills": resume_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations,
    }