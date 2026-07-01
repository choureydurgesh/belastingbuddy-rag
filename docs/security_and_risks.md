# Security and Risks – BelastingBuddy

Since BelastingBuddy handles personal and financial tax guidance queries, security and correctness are critical considerations.

## Security Posture

### Local-Only Execution
To ensure sensitive financial queries and documents remain private:
* **LLM Generation**: Ollama runs locally on `http://localhost:11434`. Queries and contexts are never sent to external AI providers (such as OpenAI, Anthropic, or Google Cloud).
* **Storage**: The ChromaDB vector database runs locally as a persistent file-based client storing data in [vectorstore/](file:///Users/durgeshchourey/Documents/rag-project/belastingbuddy-rag/vectorstore/).
* **API Server**: The FastAPI backend runs locally and does not expose ports to the public internet by default.

---

## Identified Risks and Mitigations

### 1. Hallucination of Tax Rules
* **Risk**: The local LLM could generate incorrect deadlines, brackets, or requirements.
* **Mitigation**: The system instructs the LLM via prompt engineering to use **ONLY** the provided context and respond with *"I could not find that in the approved sources"* if the answer is missing. Answers must also print source citations.

### 2. Outdated Tax Information
* **Risk**: Dutch tax regulations change annually. Old ingestion files lead to outdated advice.
* **Mitigation**: Source files should be dated or versioned, and a routine update procedure should clear/re-populate the ChromaDB collection for each new tax year.

### 3. PDF Parsing Quality
* **Risk**: Some PDFs have complex layouts, tables, or scanned text that standard encoders fail to read correctly.
* **Mitigation**: Plain text versions should be preferred when possible, or PDFs must be verified using extraction tests.
