from transformers import pipeline


sentiment_pipeline = pipeline(
    task="text-classification",
    model="ProsusAI/finbert",
    tokenizer="ProsusAI/finbert"
)


def analyze_financial_sentiment(text: str):
    """
    Analyze financial sentiment using FinBERT.

    Returns:
        sentiment label and confidence score
    """

    if not text.strip():
        return {
            "sentiment": "neutral",
            "confidence": 0.0
        }

    result = sentiment_pipeline(text[:512])[0]

    return {
        "sentiment": result["label"],
        "confidence": round(result["score"], 4)
    }