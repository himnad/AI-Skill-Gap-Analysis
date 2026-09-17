# Submission

## Project

AI Driven Skill Gap Analysis

## GitHub

https://github.com/himnad/AI-Skill-Gap-Analysis

## Live Demo

https://ai-skill-gap-analysis.vercel.app

## Backend

https://ai-skill-gap-analysis-production.up.railway.app

## Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- Vercel

### Backend

- Python
- FastAPI
- pdfplumber
- Gemini API
- FAISS
- Pandas
- NumPy
- Railway

## Main Features

- Resume PDF parsing
- AI-based resume skill extraction
- Job-description analysis
- Skill-gap identification
- Semantic NPTEL course recommendations
- Top 5 course recommendations
- Public deployment

## Dataset

NPTEL course catalog containing 3,351 courses.

## Demo Flow

1. Open the live application.
2. Upload a resume PDF.
3. Upload a job-description PDF.
4. Run the analysis.
5. Review extracted resume skills.
6. Review identified skill gaps.
7. Review the recommended NPTEL courses.

## Documentation

- `docs/architecture.md` — system architecture
- `docs/schema.md` — data and storage structure
- `docs/plan.md` — development plan
- `docs/decisions.md` — technical decisions
- `docs/ai-prompts.md` — AI prompt documentation

## Current Limitations

- No user authentication
- No analysis history
- No relational database
- NPTEL recommendations use available course metadata
- Course descriptions are not currently included in the dataset

## Future Improvements

- Personalized learning paths
- User progress tracking
- Analysis history
- More detailed course metadata
- Additional recommendation signals
- Database-backed course management

## Security

API keys are stored as environment variables and are not committed to the repository.

Resume and job-description files are processed temporarily by the backend and are not intentionally persisted as application records.

## Deployment Status

Frontend: Deployed on Vercel

Backend: Deployed on Railway

GitHub repository: Public