import os
import time
from pathlib import Path

import faiss
import numpy as np
from google import genai


MODEL_NAME = "gemini-embedding-001"
BATCH_SIZE = 50
DELAY_SECONDS = 22

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"
EMBEDDINGS_PATH = DATA_DIR / "nptel_embeddings.npy"


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set."
        )

    return genai.Client(api_key=api_key)


def generate_embeddings(texts: list[str]) -> np.ndarray:
    """
    Generate Gemini embeddings in batches.

    Previously completed batches are saved to disk so progress
    can be recovered if the API quota is reached.
    """

    if not texts:
        return np.empty((0, 3072), dtype=np.float32)

    client = get_client()
    total = len(texts)

    completed_vectors = []

    if EMBEDDINGS_PATH.exists():
        existing = np.load(EMBEDDINGS_PATH)

        if existing.ndim == 2 and existing.shape[1] == 3072:
            completed_count = existing.shape[0]

            if completed_count <= total:
                completed_vectors.append(existing)

                print(
                    f"Resuming from {completed_count}/{total} "
                    "completed embeddings."
                )

                if completed_count == total:
                    return existing

                start_position = completed_count
            else:
                start_position = 0
                completed_vectors = []
        else:
            start_position = 0
    else:
        start_position = 0

    for start in range(start_position, total, BATCH_SIZE):
        batch = texts[start:start + BATCH_SIZE]

        print(
            f"Embedding courses "
            f"{start + 1}-{min(start + BATCH_SIZE, total)} "
            f"of {total}..."
        )

        while True:
            try:
                response = client.models.embed_content(
                    model=MODEL_NAME,
                    contents=batch,
                )

                batch_vectors = np.array(
                    [embedding.values for embedding in response.embeddings],
                    dtype=np.float32,
                )

                faiss.normalize_L2(batch_vectors)

                completed_vectors.append(batch_vectors)

                all_vectors = np.vstack(completed_vectors)

                np.save(EMBEDDINGS_PATH, all_vectors)

                print(
                    f"Saved progress: "
                    f"{all_vectors.shape[0]}/{total}"
                )

                break

            except Exception as error:
                if "429" not in str(error):
                    raise

                print(
                    f"Rate limit reached. Waiting "
                    f"{DELAY_SECONDS} seconds..."
                )

                time.sleep(DELAY_SECONDS)

        if start + BATCH_SIZE < total:
            print(
                f"Waiting {DELAY_SECONDS} seconds "
                "before next batch..."
            )
            time.sleep(DELAY_SECONDS)

    vectors = np.vstack(completed_vectors)

    faiss.normalize_L2(vectors)

    np.save(EMBEDDINGS_PATH, vectors)

    return vectors


def generate_query_embedding(text: str) -> np.ndarray:
    """
    Generate a normalized embedding for a recommendation query.

    This is kept separate from the course-embedding checkpoint so
    searching does not modify nptel_embeddings.npy.
    """
    client = get_client()

    response = client.models.embed_content(
        model=MODEL_NAME,
        contents=text,
    )

    vector = np.array(
        response.embeddings[0].values,
        dtype=np.float32,
    ).reshape(1, -1)

    # Normalized vector + inner product = cosine similarity.
    faiss.normalize_L2(vector)

    return vector