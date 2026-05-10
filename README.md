# AI Financial Assistant

An AI-powered financial document assistant that allows users to upload financial PDFs, ask questions, receive grounded answers with citations, and analyze financial sentiment using FinBERT.

---

## Project Overview

This project helps users quickly understand financial documents such as annual reports, earnings reports, investor presentations, and financial filings.

Instead of manually reading long documents, users can upload a PDF and ask financial questions. The system retrieves relevant context, reranks it, and generates grounded answers with citations.

---

## Features

- Upload financial PDF documents
- Extract text page by page
- Chunk documents with overlap
- Generate embeddings using Jina AI
- Store vectors in Qdrant Cloud
- Retrieve relevant chunks using semantic search
- Rerank retrieved chunks using Jina Reranker
- Generate grounded answers using Gemini
- Show citation-based sources
- Analyze financial sentiment using FinBERT
- FastAPI backend
- Streamlit frontend
- Clear/reset vector database option

---

## Tech Stack

- Python
- FastAPI
- Streamlit
- Qdrant Cloud
- Jina Embeddings
- Jina Reranker
- Gemini API
- FinBERT
- Hugging Face Transformers
- PyMuPDF
- Requests

---

## Architecture

```text
User Uploads PDF
        ↓
PDF Text Extraction
        ↓
Text Chunking
        ↓
Jina Embeddings
        ↓
Qdrant Vector Database
        ↓
User Question
        ↓
Query Embedding
        ↓
Semantic Retrieval
        ↓
Jina Reranking
        ↓
Gemini Financial Reasoning
        ↓
Answer with Citations
```
---

## Sentiment Analysis Flow
```text
Financial Text / News / Headline
        ↓
FinBERT Model
        ↓
Positive / Negative / Neutral Sentiment
        ↓
Confidence Score
```
---

## Project Structure
```text
ai-financial-assistant/
│
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── chunker.py
│   │   └── embedder.py
│   ├── vectorstore/
│   │   └── vector_store.py
│   ├── retrieval/
│   │   ├── retriever.py
│   │   └── reranker.py
│   ├── llm/
│   │   └── financial_reasoner.py
│   ├── sentiment/
│   │   └── finbert_sentiment.py
│   └── pipelines/
│       └── rag_pipeline.py
│
├── frontend/
│   └── app.py
│
├── data/
│   └── uploads/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

```
---

## Environment Variables

Create a .env file in the root directory:

GEMINI_API_KEY=your_gemini_api_key
JINA_API_KEY=your_jina_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key

Never upload .env to GitHub.

---

## How to Run Locally
### 1. Clone the Repository
git clone https://github.com/Shivraj207/ai-financial-assistant.git
cd ai-financial-assistant
### 2. Create Virtual Environment
python -m venv venv
source venv/bin/activate

For Windows:
venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt
### 4. Add Environment Variables

Create a .env file and add your API keys.

### 5. Run FastAPI Backend
uvicorn backend.main:app --reload

Backend runs at:
http://127.0.0.1:8000

API docs:
http://127.0.0.1:8000/docs

---

### 6. Run Streamlit Frontend

Open a second terminal:
streamlit run frontend/app.py

Frontend runs at:
http://localhost:8501

---

## Example Questions
What are the major risk factors mentioned in the report?
What risks are associated with foreign exchange rates?
How could macroeconomic conditions affect the company?
What are the company’s major revenue sources?

---

## Example Sentiment Inputs
Apple reported strong revenue growth and improved margins this quarter.
The company warned about declining demand and lower profit margins.

---

## Key Learning Outcomes
Built an end-to-end RAG pipeline
Integrated vector search using Qdrant
Used embeddings for semantic retrieval
Improved retrieval quality using reranking
Built a FastAPI backend and Streamlit frontend
Added financial sentiment analysis using FinBERT
Designed citation-based grounded financial answers

---

## Future Improvements
Multi-document comparison
Financial ratio extraction
Risk severity scoring
Conversation memory
Better citation formatting
Cloud deployment
Authentication
Dashboard analytics
Disclaimer

---

## Advice
This project is for educational and portfolio purposes only. It does not provide financial advice or investment recommendations.
