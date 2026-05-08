from typing import List, Dict

from backend.ingestion.embedder import embed_query
from backend.vectorstore.vector_store import search_similar
from backend.config import TOP_K_RETRIEVAL


def retrieve_chunks(query: str) -> List[Dict]:
    """
    Retrieve top relevant chunks for a user query.
    """

    if not query.strip():
        return []

    query_embedding = embed_query(query)

    if not query_embedding:
        return []

    results = search_similar(
        query_embedding=query_embedding,
        top_k=TOP_K_RETRIEVAL
    )

    return results