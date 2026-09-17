# Technical Decisions

## 1. FastAPI for the Backend

### Chosen

FastAPI was selected for the backend API.

### Rejected Alternatives

A traditional Flask implementation was not used for the final backend.

### Why

FastAPI provides straightforward file-upload endpoints, automatic OpenAPI documentation, and works well with the Python-based AI pipeline.

---

## 2. Next.js for the Frontend

### Chosen

Next.js with React and TypeScript.

### Why

The application benefits from a modern React interface while keeping the frontend independently deployable on Vercel.

---

## 3. Gemini Instead of OpenAI

### Initial Decision

The original project design used OpenAI models for skill extraction and embeddings.

### Later Change

The implementation was changed to Gemini because OpenAI model access was not available for the final implementation.

### Final Choice

- `gemini-2.5-flash` for generation
- `gemini-embedding-001` for embeddings

### Why

Gemini provided the required generation and embedding capabilities while allowing the implementation to continue without OpenAI access.

---

## 4. FAISS for Course Retrieval

### Chosen

FAISS was selected for vector similarity search.

### Why

The NPTEL catalog is relatively small and can be efficiently searched locally using FAISS without introducing a separate vector database.

---

## 5. IndexFlatIP with Normalized Embeddings

### Initial Approach

The earlier implementation used L2-based FAISS indexing.

### Final Decision

The implementation uses normalized embeddings with `IndexFlatIP`.

### Why

Normalized vectors combined with inner product provide cosine-similarity search, which matches the intended semantic-similarity recommendation approach.

---

## 6. Local Embedding Checkpointing

### Chosen

Generated course embeddings are saved to:

`backend/data/nptel_embeddings.npy`

### Why

Embedding thousands of courses is expensive and can be interrupted by API rate limits. Saving completed batches allows the process to resume instead of starting from zero.

---

## 7. Separate Query Embeddings from Course Embeddings

### Chosen

The query embedding is generated separately and does not overwrite the course embedding checkpoint.

### Why

The persistent course embedding file must remain aligned with the NPTEL catalog. Query embeddings are temporary search inputs and should not modify the stored course embeddings.

---

## 8. Separate Frontend and Backend Deployment

### Chosen

- Frontend → Vercel
- Backend → Railway

### Why

This keeps the frontend and Python API independently deployable and matches the repository's frontend/backend separation.