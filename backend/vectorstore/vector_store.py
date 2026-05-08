import uuid
from typing import List, Dict

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from backend.config import (
    QDRANT_URL,
    QDRANT_API_KEY,
    QDRANT_COLLECTION_NAME,
    EMBEDDING_DIMENSION
)


client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    check_compatibility=False
)


def create_collection_if_not_exists() -> None:
    """
    Create Qdrant collection if it does not already exist.
    """

    existing_collections = client.get_collections().collections
    existing_names = [collection.name for collection in existing_collections]

    if QDRANT_COLLECTION_NAME not in existing_names:
        client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_DIMENSION,
                distance=Distance.COSINE
            )
        )


def upsert_chunks(
    chunks: List[Dict],
    embeddings: List[List[float]],
    batch_size: int = 64
) -> None:
    """
    Upload chunk embeddings to Qdrant in batches.
    """

    if len(chunks) != len(embeddings):
        raise ValueError("Number of chunks and embeddings must match.")

    points = []

    for chunk, embedding in zip(chunks, embeddings):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload=chunk
            )
        )

    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]

        client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=batch,
            wait=True
        )


def search_similar(
    query_embedding: List[float],
    top_k: int = 8
) -> List[Dict]:
    """
    Search similar chunks from Qdrant.
    """

    results = client.query_points(
        collection_name=QDRANT_COLLECTION_NAME,
        query=query_embedding,
        limit=top_k
    )

    return [point.payload for point in results.points]

def clear_collection() -> None:
    """
    Delete all vectors from the collection.
    """

    client.delete_collection(
        collection_name=QDRANT_COLLECTION_NAME
    )

    create_collection_if_not_exists()