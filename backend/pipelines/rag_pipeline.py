from backend.ingestion.pdf_loader import extract_text_from_pdf
from backend.ingestion.chunker import chunk_text
from backend.ingestion.embedder import embed_texts

from backend.vectorstore.vector_store import (
    create_collection_if_not_exists,
    upsert_chunks
)

from backend.retrieval.retriever import retrieve_chunks
from backend.retrieval.reranker import rerank_chunks

from backend.llm.financial_reasoner import generate_answer


def ingest_pdf(pdf_path: str):
    """
    Complete ingestion pipeline:
    PDF -> chunks -> embeddings -> Qdrant
    """

    print("\n[INFO] Extracting text from PDF...")
    pages = extract_text_from_pdf(pdf_path)

    print(f"[INFO] Extracted {len(pages)} pages")

    print("\n[INFO] Creating chunks...")
    chunks = chunk_text(pages)

    print(f"[INFO] Created {len(chunks)} chunks")

    print("\n[INFO] Generating embeddings...")
    texts = [chunk["text"] for chunk in chunks]

    embeddings = embed_texts(texts)

    print(f"[INFO] Generated {len(embeddings)} embeddings")

    print("\n[INFO] Creating Qdrant collection...")
    create_collection_if_not_exists()

    print("[INFO] Uploading vectors to Qdrant...")
    upsert_chunks(chunks, embeddings)

    print("[SUCCESS] PDF ingestion completed.")


def ask_question(query: str):
    """
    Complete RAG pipeline:
    Query -> retrieval -> reranking -> LLM answer
    """

    print("\n[INFO] Retrieving relevant chunks...")
    retrieved_chunks = retrieve_chunks(query)

    print(f"[INFO] Retrieved {len(retrieved_chunks)} chunks")

    print("\n[INFO] Reranking chunks...")
    reranked_chunks = rerank_chunks(
        query=query,
        chunks=retrieved_chunks
    )

    print(f"[INFO] Reranked to {len(reranked_chunks)} chunks")

    print("\n[INFO] Generating final answer...")
    answer, sources = generate_answer(
        query=query,
        reranked_chunks=reranked_chunks
    )

    return answer, sources