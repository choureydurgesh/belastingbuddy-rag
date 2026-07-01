# BelastingBuddy – Local RAG System

BelastingBuddy is a local retrieval-augmented generation (RAG) assistant for Dutch income tax filing guidance. It helps users understand filing steps, required documents, deadlines, and migration-year cases using trusted knowledge sources.

---

## 🛠️ Prerequisites

To run this project locally, you need:
1. **Python 3.11+**
2. **Ollama** installed on your machine.
3. **Ollama Model**: Pull the 1.5B parameter code model:
   ```bash
   ollama pull qwen2.5-coder:1.5b
   ```

---

## 🚀 Quick Start Guide

### 1. Setup Environment & Dependencies
Clone this repository, navigate to the project directory, set up your Python virtual environment, and install dependencies:
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install ingestion & database requirements
pip install -r scripts/requirements.txt
```

### 2. Ingest Source Documents
Drop any plain text (`*.txt`) or PDF (`*.pdf`) files with Dutch tax regulations into the [data/raw/](file:///Users/durgeshchourey/Documents/rag-project/belastingbuddy-rag/data/raw/) folder. Then run the ingestion script to chunk, embed, and index them into the local Chroma vector database:
```bash
python scripts/ingest.py
```

### 3. Query the System via CLI
Verify document chunk retrieval or run the full RAG generation pipeline from your terminal:

* **Test document chunk retrieval only:**
  ```bash
  python scripts/query.py "What is the M-form?"
  ```
* **Test full grounded question answering (via Ollama):**
  ```bash
  python scripts/ask.py "What is the M-form?"
  ```

---

## 🌐 Running the FastAPI Web Server

You can run the backend API server locally to power a custom frontend or integration:

```bash
# Start the server
uvicorn app.main:app --reload
```
* **Swagger Interactive Docs**: Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.
* **Test the RAG endpoint via Curl**:
  ```bash
  curl -X POST "http://localhost:8000/ask" \
       -H "Content-Type: application/json" \
       -d '{"question": "What is the M-form?"}'
  ```

---

## 🧪 Running Automated Tests

To install test runner tools and execute the unit and integration tests (validating chunking functions, endpoints, and mocking DB/Ollama operations):

```bash
# Install test tools
pip install pytest

# Run the test suite
pytest tests/
```

---

## 📁 Repository Structure

```text
belastingbuddy-rag/
├── app/
│   └── main.py                 # FastAPI API Server (endpoints /, /health, /ask)
├── data/
│   └── raw/                    # Raw tax guidelines (TXT and PDF files)
├── docs/                       # Architecture, PRD, security plans, test plans
├── scripts/
│   ├── ingest.py               # Document parsing & ingestion logic
│   ├── query.py                # Chroma DB document search tool
│   ├── ask.py                  # CLI grounded RAG client
│   └── requirements.txt        # Backend dependencies
├── tests/                      # Automated test suite (pytest)
├── vectorstore/                # Local Chroma database persistence directory
└── pytest.ini                  # Pytest environment path configuration
```
