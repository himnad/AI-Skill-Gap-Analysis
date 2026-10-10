**Live Demo:** https://ai-skill-gap-analysis.vercel.app

# AI-Driven Skill Gap Analysis



\*\*AI-powered resume-to-job-description analysis with personalized NPTEL course recommendations.\*\*



\[\*\*Live Demo\*\*](https://ai-skill-gap-analysis.vercel.app) · \[\*\*Backend API\*\*](https://ai-skill-gap-analysis-production.up.railway.app) · \[\*\*Source Code\*\*](https://github.com/himnad/AI-Skill-Gap-Analysis)



\## Overview



AI-Driven Skill Gap Analysis is a full-stack web application that compares a candidate's resume with a job description, identifies missing skills, and recommends relevant courses from a catalog of \*\*3,351 NPTEL courses\*\*.



The application combines \*\*Gemini-powered skill extraction and gap analysis\*\* with \*\*embedding-based semantic retrieval\*\* using FAISS.



\## Key Features



\- \*\*Resume and job-description upload:\*\* Accepts PDF documents through the web interface.

\- \*\*Resume skill extraction:\*\* Uses Gemini to identify skills mentioned in the resume.

\- \*\*Skill-gap identification:\*\* Compares extracted skills with job-description requirements.

\- \*\*Semantic course matching:\*\* Retrieves relevant NPTEL courses using Gemini embeddings and FAISS.

\- \*\*Top-five recommendations:\*\* Displays course names, disciplines, instructors, institutes, links, and similarity scores.

\- \*\*Deployed application:\*\* Next.js frontend on Vercel and FastAPI backend on Railway.



\## Live Application



\*\*Frontend:\*\* https://ai-skill-gap-analysis.vercel.app  

\*\*Backend:\*\* https://ai-skill-gap-analysis-production.up.railway.app



\### How to Use



1\. Open the \[live application](https://ai-skill-gap-analysis.vercel.app).

2\. Upload a resume PDF.

3\. Upload a job-description PDF.

4\. Run the analysis.

5\. Review the extracted resume skills, missing skills, and recommended NPTEL courses.



\## System Architecture



```mermaid

flowchart TD

&#x20;   A\[User uploads resume and job-description PDFs] --> B\[Next.js frontend]

&#x20;   B --> C\[FastAPI /analyze endpoint]

&#x20;   C --> D\[PDF text extraction with pdfplumber]

&#x20;   D --> E\[Gemini resume skill extraction]

&#x20;   E --> F\[Gemini skill-gap analysis]

&#x20;   F --> G\[Missing-skills recommendation query]

&#x20;   G --> H\[Gemini query embedding]

&#x20;   H --> I\[FAISS similarity search]

&#x20;   J\[3,351 NPTEL courses + precomputed embeddings] --> I

&#x20;   I --> K\[Top 5 course recommendations]

&#x20;   K --> L\[Frontend results]

```



The frontend and backend are independently deployed. The backend handles document processing, AI analysis, and course retrieval.



\## Tech Stack



| Layer | Technologies |

|---|---|

| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS |

| Backend | Python, FastAPI, Uvicorn |

| PDF processing | pdfplumber |

| AI analysis | Gemini `gemini-2.5-flash` |

| Embeddings | Gemini `gemini-embedding-001` |

| Semantic search | FAISS (`IndexFlatIP`), NumPy |

| Course data | Pandas, CSV, NumPy embeddings |

| Deployment | Vercel (frontend), Railway (backend) |



\## Recommendation Pipeline



1\. The backend extracts text from the uploaded PDFs using \*\*pdfplumber\*\*.

2\. \*\*Gemini 2.5 Flash\*\* extracts resume skills and identifies missing skills relative to the job description.

3\. Missing skills are combined into a semantic search query.

4\. \*\*`gemini-embedding-001`\*\* converts the query into an embedding.

5\. FAISS searches the precomputed NPTEL course index.

6\. The system returns the \*\*five most relevant courses\*\*.



The catalog's \*\*3,072-dimensional embeddings\*\* are normalized and indexed using FAISS \*\*`IndexFlatIP`\*\*. For normalized vectors, inner-product similarity corresponds to cosine similarity.



\## NPTEL Course Dataset



The course catalog contains \*\*3,351 courses\*\* with these metadata fields:



| Field | Description |

|---|---|

| `Discipline` | Course discipline or domain |

| `Course\_Name` | NPTEL course title |

| `Instructor\_Name` | Instructor |

| `Institute\_Name` | Offering institution |

| `Course\_URL` | Link to the course |



The data assets are located at:



```text

backend/data/nptel\_course\_catalog.csv

backend/data/nptel\_embeddings.npy

backend/data/nptel\_courses.faiss

```



\*\*Important:\*\* The CSV row order, embedding array row order, and FAISS index positions must remain aligned for recommendations to map to the correct courses. Course descriptions are not currently included in the catalog.



\## Repository Structure



```text

AI-Skill-Gap-Analysis/

├── backend/             # FastAPI application and course data

├── frontend/            # Next.js web application

├── docs/                # Architecture and design documentation

├── .gitignore

├── LICENSE

├── README.md

└── SUBMISSION.md

```



\## Local Development



\### Prerequisites



\- Python and Node.js versions compatible with the project's pinned dependencies

\- A Gemini API key

\- Required NPTEL data and FAISS index files in `backend/data/`



\### Backend



From the repository root:



```bash

cd backend

python -m venv .venv

```



Activate the environment:



\*\*Windows CMD:\*\*



```cmd

.venv\\Scripts\\activate

```



\*\*macOS/Linux:\*\*



```bash

source .venv/bin/activate

```



Install dependencies:



```bash

pip install -r requirements.txt

```



Configure the Gemini API key using the environment-variable mechanism expected by the backend. Check the backend source before choosing a variable name or launch command.



\### Frontend



In a second terminal, from the repository root:



```bash

cd frontend

npm ci

npm run dev

```



Open the local URL printed by Next.js (typically `http://localhost:3000`). Configure the frontend's backend API URL according to the application's source and deployment settings.



> \*\*Setup note:\*\* The exact FastAPI module entry point, Gemini environment-variable name, and frontend API URL variable should be confirmed from source code before adding copy-paste backend launch instructions. This README intentionally avoids guessing them.



\## API Output



The FastAPI backend exposes an \*\*`/analyze`\*\* endpoint. Its response includes:



\- `resume\_skills`

\- `missing\_skills`

\- `recommendations`



Each recommendation includes:



\- `course\_name`

\- `discipline`

\- `instructor`

\- `institute`

\- `course\_url`

\- `similarity\_score`



\## Documentation



\- \[Architecture](docs/architecture.md)

\- \[Data schema](docs/schema.md)

\- \[Development plan](docs/plan.md)

\- \[Technical decisions](docs/decisions.md)

\- \[Submission details](SUBMISSION.md)



\## Current Limitations



\- No user authentication or analysis history

\- No relational database

\- Course recommendations rely on available NPTEL metadata rather than full course descriptions

\- Course metadata and vector index are stored as local data assets



\## Future Improvements



\- Personalized learning paths and progress tracking

\- Saved analysis history

\- Richer course descriptions and additional recommendation signals

\- Database-backed course catalog management

\- Automated testing and continuous integration



\## Security and Privacy



Gemini API credentials should be provided through environment variables and \*\*must not be committed\*\* to version control. Resume and job-description PDFs are processed temporarily by the backend and are not intentionally stored as persistent application records.



\## License



Licensed under the \[MIT License](LICENSE).



