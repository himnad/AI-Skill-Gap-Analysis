# Data Schema

## Relational Database

The application does not currently use a relational database.

The main persistent dataset is the NPTEL course catalog stored as CSV.

## NPTEL Course Catalog

File:

`backend/data/nptel_course_catalog.csv`

| Column | Description |
|---|---|
| Discipline | Course discipline/domain |
| Course_Name | Name of the NPTEL course |
| Instructor_Name | Course instructor |
| Institute_Name | Institution offering the course |
| Course_URL | NPTEL course URL |

## Embedding Data

File:

`backend/data/nptel_embeddings.npy`

Contains the generated 3072-dimensional Gemini embeddings corresponding to the NPTEL catalog rows.

The row ordering must remain aligned with the CSV because FAISS result indices are mapped back to CSV rows.

## FAISS Index

File:

`backend/data/nptel_courses.faiss`

Contains the normalized course embeddings.

The index uses `IndexFlatIP`.

Because the vectors are normalized, inner-product search corresponds to cosine similarity.

## Application Output

The `/analyze` endpoint returns:

- `resume_skills`
- `missing_skills`
- `recommendations`

Each recommendation contains:

- course_name
- discipline
- instructor
- institute
- course_url
- similarity_score

## Scaling Considerations

At approximately 100x the current catalog size:

- embedding generation would require substantially more API requests
- embedding generation time and API quota would become significant
- FAISS index memory requirements would increase
- CSV loading would become less efficient
- deployment storage requirements would increase

A larger production system could move the course catalog and metadata to a database and use a dedicated vector database or distributed vector-search system.