import json
import os

from google import genai
from google.genai import types


MODEL_NAME = "gemini-2.5-flash"


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

    return genai.Client(api_key=api_key)


def extract_resume_skills(resume_text: str) -> list[str]:
    """
    Extract technical and professional skills from a resume.
    """

    prompt = f"""
You are an expert resume skill extractor.

Extract all meaningful skills from the resume below.

Rules:
- Include programming languages, frameworks, libraries, tools,
  databases, APIs, platforms, methodologies, and relevant soft skills.
- Keep each skill short and concise.
- Do not invent skills that are not supported by the resume.
- Avoid duplicate skills.
- Return ONLY a JSON array of strings.
- Do not include markdown or explanations.

RESUME:
{resume_text}
"""

    client = get_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
        ),
    )

    skills = json.loads(response.text)

    if not isinstance(skills, list):
        raise ValueError("Gemini did not return a list of skills.")

    return [str(skill).strip() for skill in skills if str(skill).strip()]


def extract_missing_skills(
    job_description: str,
    resume_skills: list[str],
) -> list[str]:
    """
    Compare the candidate's skills with the job description
    and identify important missing skills.
    """

    prompt = f"""
You are an expert technical recruiter performing skill-gap analysis.

JOB DESCRIPTION:
{job_description}

CANDIDATE'S CURRENT SKILLS:
{json.dumps(resume_skills)}

Identify the important skills required by the job description
that are missing or insufficiently demonstrated in the candidate's
current skills.

Rules:
- Focus on meaningful job-relevant skills.
- Do not invent requirements that are not present in the job description.
- Do not list skills the candidate already clearly has.
- Keep each missing skill short and concise.
- Avoid duplicates.
- Return ONLY a JSON array of strings.
- Do not include markdown or explanations.
"""

    client = get_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
        ),
    )

    missing_skills = json.loads(response.text)

    if not isinstance(missing_skills, list):
        raise ValueError("Gemini did not return a list of missing skills.")

    return [
        str(skill).strip()
        for skill in missing_skills
        if str(skill).strip()
    ]