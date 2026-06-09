import sys
from pathlib import Path
import chromadb

BASE = Path(__file__).resolve().parents[1]
DB_DIR = BASE / "vectorstore"

client = chromadb.PersistentClient(path=str(DB_DIR))
collection = client.get_collection(name="belastingbuddy_docs")

query = " ".join(sys.argv[1:]).strip() or "What is the M-form and when is it used?"
results = collection.query(query_texts=[query], n_results=3)

print("QUERY:", query)

for idx, doc in enumerate(results["documents"][0], start=1):
    meta = results["metadatas"][0][idx - 1]
    print(f"\nResult {idx}")
    print("Source:", meta["source_file"])
    print("Chunk:", meta["chunk_index"])
    print(doc)
