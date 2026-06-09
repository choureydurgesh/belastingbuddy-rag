import sys
from pathlib import Path
import requests
import chromadb

BASE = Path(__file__).resolve().parents[1]
DB_DIR = BASE / "vectorstore"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:1.5b"
COLLECTION_NAME = "belastingbuddy_docs"

client = chromadb.PersistentClient(path=str(DB_DIR))
collection = client.get_or_create_collection(name=COLLECTION_NAME)

if collection.count() == 0:
    print("Collection is empty. Run: python scripts/ingest.py")
    raise SystemExit(1)

question = " ".join(sys.argv[1:]).strip() or "What documents are needed before filing Dutch income tax?"

results = collection.query(
    query_texts=[question],
    n_results=3,
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

context_text = "\n\n".join(context_blocks)

prompt = f"""
You are BelastingBuddy, a Dutch tax filing guidance assistant.

Answer the user's question using ONLY the context below.
If the answer is not in the context, say:
"I could not find that in the approved sources."

Keep the answer short, clear, and practical.
At the end, add a line starting with 'Sources:' and list the source names.

Context:
{context_text}

User question:
{question}
""".strip()

payload = {
    "model": MODEL,
    "prompt": prompt,
    "stream": False,
    "options": {
        "temperature": 0.2,
        "num_predict": 250
    }
}

response = requests.post(OLLAMA_URL, json=payload, timeout=120)
response.raise_for_status()
data = response.json()

print("\nQUESTION:\n", question)
print("\nANSWER:\n", data["response"].strip())
print("\nRETRIEVED SOURCES:")
for s in sources:
    print("-", s)
