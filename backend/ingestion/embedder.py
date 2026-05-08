import requests
from typing import List

from backend.config import JINA_API_KEY


JINA_EMBED_URL = "https://api.jina.ai/v1/embeddings"


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts using Jina AI.
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JINA_API_KEY}"
    }

    payload = {
        "model": "jina-embeddings-v3",
        "input": texts
    }

    try:

        response = requests.post(
            JINA_EMBED_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()["data"]

        embeddings = [
            item["embedding"]
            for item in data
        ]

        return embeddings

    except Exception as e:

        print(f"[ERROR] Embedding generation failed: {e}")

        return []


def embed_query(query: str) -> List[float]:
    """
    Generate embedding for a single query.
    """

    embedding = embed_texts([query])

    return embedding[0] if embedding else []