from pathlib import Path

import faiss
import numpy as np
import pandas as pd

from app.services.embedding_service import generate_embeddings


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"

CSV_PATH = DATA_DIR / "nptel_course_catalog.csv"
INDEX_PATH = DATA_DIR / "nptel_courses.faiss"
EMBEDDINGS_PATH = DATA_DIR / "nptel_embeddings.npy"


def build_course_index():
    """
    Build a FAISS index from the NPTEL course catalog.

    Embeddings are saved locally so completed work can be reused.
    """

    df = pd.read_csv(CSV_PATH)

    required_columns = [
        "Discipline",
        "Course_Name",
        "Instructor_Name",
        "Institute_Name",
        "Course_URL",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    course_texts = (
        "Course: " + df["Course_Name"].fillna("") +
        "\nDiscipline: " + df["Discipline"].fillna("") +
        "\nInstructor: " + df["Instructor_Name"].fillna("") +
        "\nInstitute: " + df["Institute_Name"].fillna("")
    ).tolist()

    total = len(course_texts)

    # Reuse previously saved embeddings if they exist.
    if EMBEDDINGS_PATH.exists():
        vectors = np.load(EMBEDDINGS_PATH)

        if vectors.shape[0] == total:
            print(
                f"Found existing embeddings for {total} courses."
            )
        else:
            print("Existing embeddings do not match dataset.")
            print("Regenerating embeddings...")
            vectors = generate_embeddings(course_texts)
            np.save(EMBEDDINGS_PATH, vectors)
    else:
        print(f"Generating embeddings for {total} courses...")
        vectors = generate_embeddings(course_texts)
        np.save(EMBEDDINGS_PATH, vectors)
        print(f"Embeddings saved to: {EMBEDDINGS_PATH}")

    print(f"Embedding shape: {vectors.shape}")

    # Normalized vectors + inner product = cosine similarity.
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    faiss.write_index(index, str(INDEX_PATH))

    print(f"FAISS index saved to: {INDEX_PATH}")
    print(f"Courses indexed: {index.ntotal}")

    return index


if __name__ == "__main__":
    build_course_index()