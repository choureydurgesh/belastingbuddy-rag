# BelastingBuddy Local RAG Implementation Guide

## Goal

The first goal is to get local chat working, then connect Dutch tax documents after that. Open WebUI is a good first UI because it is designed to run locally and connect to Ollama before moving to a custom frontend.

## Implementation flow

Use this sequence for the first working version:

1. Install Ollama on macOS.
2. Pull and test one local model.
3. Run Open WebUI and connect it to Ollama.
4. Verify that local chat works.
5. Move to ingestion and retrieval with Chroma.

## Ollama setup on macOS

Install Ollama with Homebrew and start the service:

```bash
brew install ollama
brew services start ollama
```

Then test the local endpoint. Ollama uses a local API endpoint on `http://localhost:11434`.

## First local model

Pull a small model so setup is fast and responsive on a laptop.

```bash
ollama pull qwen2.5-coder:1.5b
ollama run qwen2.5-coder:1.5b
```

A smaller model is useful for validating the local stack first; larger models can be tested later after the full workflow is stable.

## Open WebUI setup

Open WebUI supports Ollama and can be started with Docker, pip, uv, or desktop, while Docker is presented as the fastest recommended path in the quick-start flow.A pip-based install can work, but the project guidance recommends Python 3.11 for pip installation.

```bash
pip install open-webui
open-webui serve
```

This normally exposes the UI at `http://localhost:8080`.

### Python troubleshooting

If pip installation fails, check Python 3.11 first because Open WebUI pip installation guidance recommends that version.

```bash
python3.11 --version
```

If Python 3.11 is available, create and activate a virtual environment, upgrade pip, then install Open WebUI:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install open-webui
open-webui serve
```

After startup, open `http://localhost:8080`, create credentials, and verify that the UI loads correctly.

## Connect Open WebUI to Ollama

First confirm that Ollama is running:

```bash
ollama list
```

If Ollama is not available, start it again:

```bash
brew services start ollama
```

For additional testing, another small model can be pulled and verified:

```bash
ollama pull llama3.2:1b
ollama list
```

Then open Open WebUI, select the Ollama model from the model dropdown, and send a simple prompt such as `Say hello` to verify the local chat path works.

## Repository structure

Use this project structure for the BelastingBuddy prototype:

```text
belastingbuddy-rag/
├── data/
│   └── raw/
│       ├── tax_deadlines.txt
│       └── m_form.txt
├── scripts/
│   ├── requirements.txt
│   ├── ingest.py
│   ├── query.py
│   └── ask.py
└── vectorstore/
```

The raw source files provide the first knowledge base, the scripts folder contains ingestion and query logic, and the vectorstore folder holds the persisted Chroma data.

## Chroma setup

Create the raw source files in `data/raw/` and install dependencies inside the project virtual environment.

```bash
cd ~/belastingbuddy-rag
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
```

Chroma supports creating persistent collections, storing documents with IDs and metadata, and querying them by natural language.

## Ingestion and retrieval

Run the scripts from the repository root in this order so the collection exists before querying it:

```bash
cd ~/belastingbuddy-rag
source .venv/bin/activate
python scripts/ingest.py
python scripts/query.py "What documents are needed before filing Dutch income tax?"
```

The order matters because the ingestion step creates and populates the Chroma collection, and the query step depends on that collection being present.

## Add ask.py for full RAG flow

After retrieval works, add `scripts/ask.py` so the top retrieved chunks are sent to Ollama for grounded answer generation. Ollama's generate API accepts a POST request with model name, prompt, and `stream: false` for a single JSON response.

Install one extra package:

```bash
pip install requests
```

Then test the full RAG flow:

```bash
python scripts/ask.py "What documents are needed before filing Dutch income tax?"
```

This produces the first complete local flow: question, retrieval from Chroma, prompt construction, generation through Ollama, and final answer.

## Working order

Always run commands in this order during development

```bash
source .venv/bin/activate
python scripts/ingest.py
python scripts/query.py "What documents are needed before filing Dutch income tax?"
python scripts/ask.py "What documents are needed before filing Dutch income tax?"
```

## Running Tests

To verify that the ingestion and backend API routing are working correctly, run the automated test suite:

```bash
pytest tests/
```

## Next steps

After the local RAG flow and FastAPI backend are working, the next steps are:

- Improve chunking and metadata quality for better retrieval.
- Add real official Dutch tax documents (TXT or PDF formats) to `data/raw/` instead of starter sample files.
- Build or connect a custom frontend to the FastAPI `/ask` endpoint (or use Open WebUI).
