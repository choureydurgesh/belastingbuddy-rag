from pathlib import Path
import requests
import chromadb
from fastapi import FastAPI
from pydantic import BaseModel

BASE = Path(__file__).resolve().parents[1]
DB_DIR = BASE / "vectorstore"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:1.5b"
COLLECTION_NAME = "belastingbuddy_docs"

app = FastAPI(title="BelastingBuddy API", version="0.1.0")

client = chromadb.PersistentClient(path=str(DB_DIR))
collection = client.get_or_create_collection(name=COLLECTION_NAME)

class AskRequest(BaseModel):
    question: str
    top_k: int = 3

@app.get("/")
def root():
    return {"message": "BelastingBuddy API is running"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "collection_count": collection.count()
    }

@app.post("/ask")
def ask(req: AskRequest):
    if collection.count() == 0:
        return {
            "answer": "Collection is empty. Run python scripts/ingest.py first.",
            "sources": []
        }

    results = collection.query(
        query_texts=[req.question],
        n_results=req.top_k,
        include=["documents", "metadatas"]
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    context_blocks = []
    sources = []

    for i, (doc, meta) in enumerate(zip(docs, metas), start=1):
        source = f"{meta['source_file']}#chunk-{meta['chunk_index']}"
        sources.append(source)
        context_blocks.append(f"[Source {i}: {source}]\n{doc}")

    prompt = f"""
You are BelastingBuddy, a Dutch tax filing guidance assistant.
Answer the user's question using ONLY the context below.
If the answer is not in the context, say: I could not find that in the approved sources.
Keep the answer short, clear, and practical.
At the end, add a line starting with 'Sources:' and list the source names.

Context:
{chr(10).join(context_blocks)}

User question:
{req.question}
""".strip()

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 250
            }
        },
        timeout=120
    )
    response.raise_for_status()

    return {
        "answer": response.json()["response"].strip(),
        "sources": sources
    }
