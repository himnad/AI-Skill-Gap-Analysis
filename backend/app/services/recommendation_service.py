from pathlib import Path

import faiss
import pandas as pd

from app.services.embedding_service import generate_query_embedding


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

CSV_PATH = DATA_DIR / "nptel_course_catalog.csv"
INDEX_PATH = DATA_DIR / "nptel_courses.faiss"


def recommend_courses(
    skill_gaps: list[str],
    top_k: int = 5,
) -> list[dict]:
    """
    Recommend NPTEL courses based on the candidate's skill gaps.

    Args:
        skill_gaps: Skills missing from the candidate's resume.
        top_k: Number of courses to return.

    Returns:
        List of recommended courses with similarity scores.
    """

    if not skill_gaps:
        return []

    # Load the NPTEL catalog.
    df = pd.read_csv(CSV_PATH)

    # Load the already-built FAISS index.
    index = faiss.read_index(str(INDEX_PATH))

    # Combine all missing skills into one search query.
    query = "Skills to learn: " + ", ".join(skill_gaps)

    # Generate a normalized Gemini embedding for the query.
    query_vector = generate_query_embedding(query)

    # Search the FAISS index.
    scores, indices = index.search(query_vector, top_k)

    recommendations = []

    for score, index_position in zip(scores[0], indices[0]):
        if index_position < 0 or index_position >= len(df):
            continue

        course = df.iloc[int(index_position)]

        recommendations.append(
            {
                "course_name": str(course["Course_Name"]),
                "discipline": str(course["Discipline"]),
                "instructor": str(course["Instructor_Name"]),
                "institute": str(course["Institute_Name"]),
                "course_url": str(course["Course_URL"]),
                "similarity_score": round(float(score), 4),
            }
        )

    return recommendations