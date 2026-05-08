from transformers import pipeline


'''sentiment_pipeline = pipeline(
    task="text-classification",
    model="ProsusAI/finbert",
    tokenizer="ProsusAI/finbert"
)'''

sentiment_pipeline = None


def get_pipeline():
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

    result = sentiment_pipeline(text[:512])[0]

    return {
        "sentiment": result["label"],
        "confidence": round(result["score"], 4)
    }