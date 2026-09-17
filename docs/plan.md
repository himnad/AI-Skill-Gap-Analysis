# Development Plan

## Phase 1 — Project Setup

- Create project structure
- Set up FastAPI backend
- Set up Next.js frontend
- Configure Python virtual environment
- Install required dependencies

## Phase 2 — Resume and JD Processing

- Implement PDF text extraction
- Implement resume skill extraction
- Implement job-description skill-gap analysis
- Connect Gemini API

## Phase 3 — NPTEL Recommendation System

- Prepare NPTEL course catalog
- Generate course embeddings
- Store embeddings locally
- Build FAISS index
- Implement similarity-based course recommendation

## Phase 4 — Integration

- Connect frontend with FastAPI
- Implement PDF upload interface
- Display extracted skills
- Display missing skills
- Display top 5 NPTEL recommendations

## Phase 5 — Testing

- Test PDF extraction
- Test Gemini skill extraction
- Test skill-gap analysis
- Test FAISS recommendations
- Test complete `/analyze` workflow

## Phase 6 — Deployment

- Push source code to GitHub
- Deploy FastAPI backend on Railway
- Configure Railway root directory as `/backend`
- Deploy Next.js frontend on Vercel
- Connect frontend to Railway backend
- Test public deployment

## Time Tracking

Exact implementation time was not tracked consistently, so fabricated hour estimates are intentionally not included.

## Scope Cuts

The current implementation does not include:

- User accounts
- Persistent user analysis history
- A relational database
- Detailed course-description embeddings
- Personalized learning plans
- Automated progress tracking

These can be considered future improvements.