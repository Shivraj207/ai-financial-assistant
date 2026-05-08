from transformers import pipeline

# Lazy-loaded pipeline
sentiment_pipeline = None


def get_pipeline():
    """
    Load FinBERT pipeline only when needed.
    Helps reduce startup memory usage on deployment.
    """
    global sentiment_pipeline

    if sentiment_pipeline is None:
        sentiment_pipeline = pipeline(
            task="text-classification",
            model="ProsusAI/finbert",
            tokenizer="ProsusAI/finbert"
        )

    return sentiment_pipeline


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

    # Load model only when required
    pipe = get_pipeline()

    # Limit input length
    result = pipe(text[:512])[0]

    return {
        "sentiment": result["label"],
        "confidence": round(result["score"], 4)
    }