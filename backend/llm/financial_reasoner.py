from typing import List, Dict, Tuple

from google import genai

from backend.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(
    query: str,
    reranked_chunks: List[Dict]
) -> Tuple[str, List[Dict]]:
    """
    Generate grounded financial answer using retrieved context.
    """

    if not reranked_chunks:
        return (
            "I could not find relevant information in the uploaded financial documents.",
            []
        )

    context_parts = []
    sources = []

    for idx, chunk in enumerate(reranked_chunks, start=1):

        context_parts.append(
            f"[{idx}] Page {chunk['page']}:\n{chunk['text']}"
        )

        sources.append({
            "citation": f"[{idx}]",
            "page": chunk["page"],
            "text": chunk["text"]
        })

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an AI Financial Assistant.

Your responsibilities:
- Answer financial and business-related questions
- Use ONLY the provided context
- Do NOT hallucinate or invent financial information
- Explain risks, trends, and insights clearly
- If information is insufficient, say so honestly
- Use inline citations like [1], [2]

Context:
{context}

Question:
{query}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        answer = response.text.strip()

        return answer, sources

    except Exception as e:

        return f"[ERROR] Failed to generate answer: {e}", []