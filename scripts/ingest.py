from pathlib import Path
import chromadb
from pypdf import PdfReader

BASE = Path(__file__).resolve().parents[1]
RAW_DIR = BASE / "data" / "raw"
DB_DIR = BASE / "vectorstore"

client = chromadb.PersistentClient(path=str(DB_DIR))
collection = client.get_or_create_collection(name="belastingbuddy_docs")

def chunk_text(text, chunk_size=220, overlap=40):
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end].strip())
        if end == len(text):
            break
        start = max(0, end - overlap)
    return [c for c in chunks if c]

def extract_text_from_pdf(pdf_path: Path) -> str:
    reader = PdfReader(pdf_path)
    text_parts = []
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text_parts.append(extracted)
    return "\n".join(text_parts).strip()

ids, docs, metas = [], [], []

# Scan for both TXT and PDF files in the raw data directory
files = sorted(list(RAW_DIR.glob("*.txt")) + list(RAW_DIR.glob("*.pdf")))

for path in files:
    if path.suffix == ".txt":
        text = path.read_text(encoding="utf-8").strip()
    elif path.suffix == ".pdf":
        text = extract_text_from_pdf(path)
    else:
        continue

    for i, chunk in enumerate(chunk_text(text)):
        ids.append(f"{path.stem}-{i}")
        docs.append(chunk)
        metas.append({
            "source_file": path.name,
            "chunk_index": i,
            "topic": path.stem
        })

if ids:
    existing = set(collection.get(include=[]).get("ids", []))
    new_ids, new_docs, new_metas = [], [], []
    for i, d, m in zip(ids, docs, metas):
        if i not in existing:
            new_ids.append(i)
            new_docs.append(d)
            new_metas.append(m)

    if new_ids:
        collection.add(ids=new_ids, documents=new_docs, metadatas=new_metas)

print(f"Collection count: {collection.count()}")

