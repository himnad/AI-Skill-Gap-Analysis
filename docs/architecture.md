# Architecture

## Overview

AI Driven Skill Gap Analysis is a web application that analyzes a candidate's resume against a job description, identifies missing skills, and recommends relevant NPTEL courses.

## System Components

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- Deployed on Vercel

The frontend provides the interface for uploading the resume and job description and displaying the analysis results.

### Backend

- Python
- FastAPI
- pdfplumber
- Gemini API
- FAISS
- Pandas
- NumPy
- Deployed on Railway

The backend exposes the `/analyze` endpoint and performs the complete analysis pipeline.

### AI Layer

Gemini is used for:

1. Resume skill extraction
2. Job-description skill-gap analysis

The application uses `gemini-2.5-flash` for these tasks.

### Recommendation Layer

Course recommendations use:

- `gemini-embedding-001`
- FAISS
- Cosine-similarity search

The NPTEL catalog contains 3,351 courses.

Course embeddings are normalized and stored in a FAISS `IndexFlatIP` index. Normalized vectors with inner product provide cosine-similarity search.

## Data

The NPTEL catalog is stored as:

- `backend/data/nptel_course_catalog.csv`
- `backend/data/nptel_embeddings.npy`
- `backend/data/nptel_courses.faiss`

The catalog contains:

- Discipline
- Course_Name
- Instructor_Name
- Institute_Name
- Course_URL

The current catalog does not contain detailed course descriptions, so embeddings are generated from the available course metadata.

## Request Flow

1. User uploads a resume PDF and job-description PDF.
2. Frontend sends both files to the FastAPI `/analyze` endpoint.
3. Backend extracts PDF text using pdfplumber.
4. Gemini extracts skills from the resume.
5. Gemini identifies missing skills from the job description.
6. Missing skills are combined into a recommendation query.
7. Gemini generates an embedding for the query.
8. FAISS searches the NPTEL course index.
9. Top 5 courses are returned.
10. Frontend displays the skills, gaps, and recommendations.

## Deployment

- Frontend: Vercel
- Backend: Railway
- Source code: GitHub

## Why This Structure

The frontend and backend are separated so they can be deployed independently.

Railway uses `/backend` as its root directory because the repository is a monorepo containing both frontend and backend code.