import os
from dotenv import load_dotenv

load_dotenv()

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Jina
JINA_API_KEY = os.getenv("JINA_API_KEY")

# Qdrant
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Collection
QDRANT_COLLECTION_NAME = "financial_documents"

# Embedding dimension
EMBEDDING_DIMENSION = 1024

# Retrieval settings
TOP_K_RETRIEVAL = 8
TOP_K_RERANK = 4