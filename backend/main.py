import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.vectorstore.vector_store import clear_collection
from backend.sentiment.finbert_sentiment import analyze_financial_sentiment

from backend.pipelines.rag_pipeline import ingest_pdf, ask_question


app = FastAPI(
    title="AI Financial Assistant",
    description="RAG-based financial document Q&A assistant with citations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "AI Financial Assistant backend is running"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and ingest financial PDF.
    """

    if not file.filename.endswith(".pdf"):
        return {
            "error": "Only PDF files are supported."
        }

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_pdf(file_path)

    return {
        "message": "PDF uploaded and processed successfully.",
        "filename": file.filename
    }


@app.post("/ask")
async def ask(query: str = Form(...)):
    """
    Ask question from uploaded financial documents.
    """

    answer, sources = ask_question(query)

    return {
        "query": query,
        "answer": answer,
        "sources": sources
    }

@app.delete("/reset")
async def reset_database():
    """
    Clear all stored vectors from Qdrant.
    """

    clear_collection()

    return {
        "message": "Vector database cleared successfully."
    }
    
@app.post("/sentiment")
async def sentiment_analysis(text: str = Form(...)):
    """
    Analyze financial sentiment from text.
    """

    result = analyze_financial_sentiment(text)

    return {
        "text": text,
        "sentiment": result["sentiment"],
        "confidence": result["confidence"]
    }