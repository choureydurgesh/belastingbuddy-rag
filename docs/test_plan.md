# Test Plan – BelastingBuddy

This document describes how to test the BelastingBuddy RAG pipeline and FastAPI backend services.

## Automated Testing

An automated test suite is configured using `pytest` to test backend endpoints and ingestion helpers.

### Prerequisites

Ensure you install the required dependencies (including `pytest` and `httpx`):
```bash
pip install pytest httpx
```

### Running Tests

To run the automated tests, run this command from the project root:
```bash
pytest tests/
```

This will run:
* **Unit Tests for Ingestion (`tests/test_ingest.py`):** Tests the text chunking mechanism ([chunk_text](file:///Users/durgeshchourey/Documents/rag-project/belastingbuddy-rag/scripts/ingest.py#L11-L20)) to verify bounds, overlaps, and string lengths.
* **Integration Tests for API (`tests/test_main.py`):** Tests the FastAPI endpoints (`GET /`, `GET /health`, and `POST /ask`) with mocked database calls and mocked LLM (Ollama) HTTP responses to verify the request-response routing works correctly.

---

## Manual Testing

### 1. Ingestion Pipeline
To test the ingestion flow from raw data files to the Chroma vector database:
```bash
python scripts/ingest.py
```
This should read `.txt` files under `data/raw/` and populate/create the Chroma collection.

### 2. Search Retrieval
To verify that semantic search and document retrieval are functioning:
```bash
python scripts/query.py "What is the M-form?"
```

### 3. End-to-End RAG (Ollama Generation)
Make sure Ollama is running and has the model pulled:
```bash
ollama run qwen2.5-coder:1.5b
```
Then run the RAG query script:
```bash
python scripts/ask.py "What is the M-form?"
```

### 4. Interactive API Playground
Run the API web server:
```bash
uvicorn app.main:app --reload
```
Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view and test endpoints interactively.
