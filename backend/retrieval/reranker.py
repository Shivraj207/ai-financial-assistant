import requests
from typing import List, Dict

from backend.config import JINA_API_KEY, TOP_K_RERANK


JINA_RERANK_URL = "https://api.jina.ai/v1/rerank"


def remove_duplicate_chunks(chunks: List[Dict]) -> List[Dict]:
    """
    Remove duplicate chunks based on page number and text.
    """

    unique_chunks = []
    seen = set()

    for chunk in chunks:
        key = (
            chunk.get("page"),
            chunk.get("text", "").strip()
        )

        if key not in seen:
            seen.add(key)
            unique_chunks.append(chunk)

    return unique_chunks


def rerank_chunks(query: str, chunks: List[Dict]) -> List[Dict]:
    """
    Rerank retrieved chunks using Jina reranker.
    """

    if not query.strip() or not chunks:
        return []

    chunks = remove_duplicate_chunks(chunks)

    documents = [chunk["text"] for chunk in chunks]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JINA_API_KEY}"
    }

    payload = {
        "model": "jina-reranker-v2-base-multilingual",
        "query": query,
        "documents": documents,
        "top_n": min(TOP_K_RERANK, len(documents))
    }

    try:
        response = requests.post(
            JINA_RERANK_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        rerank_results = response.json()["results"]

        final_chunks = []

        for item in rerank_results:
            idx = item["index"]

            chunk = chunks[idx].copy()
            chunk["rerank_score"] = item["relevance_score"]

            final_chunks.append(chunk)

        return remove_duplicate_chunks(final_chunks)

    except Exception as e:
        print(f"[ERROR] Reranking failed: {e}")
        return chunks[:TOP_K_RERANK]