# Data Sources – BelastingBuddy

BelastingBuddy uses retrieval-augmented generation (RAG) powered by local knowledge files stored in the repository.

## Current Data Sources

All source files are stored in [data/raw/](file:///Users/durgeshchourey/Documents/rag-project/belastingbuddy-rag/data/raw/):

1. **`m_form.txt`**: Guide on when and why to file using the M-form (Migration Form), which is relevant for taxpayers who moved to or from the Netherlands during the tax year.
2. **`tax_deadlines.txt`**: Guide containing deadlines, general filing procedures, online portal info, and preparations for filing Dutch income taxes.

## Supported Formats

The ingestion pipeline supports reading and processing two formats:
* **Plain Text (`*.txt`)**: Parsed directly using standard Python UTF-8 file reading.
* **Portable Document Format (`*.pdf`)**: Extracted page-by-page using the `pypdf` library, making it easy to drop official tax brochures or forms directly into the pipeline.

## Ingestion Pipeline

The ingestion process is executed via [ingest.py](file:///Users/durgeshchourey/Documents/rag-project/belastingbuddy-rag/scripts/ingest.py):
1. Scan the `data/raw/` directory for `.txt` and `.pdf` files.
2. Extract text (concatenating all pages for PDF).
3. Split the text into overlapping chunks using `chunk_text()` (default size of 220 characters, 40 overlap).
4. Store chunks and source metadata (e.g. filename, chunk index) into a local ChromaDB collection (`belastingbuddy_docs`).
