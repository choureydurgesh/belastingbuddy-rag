# Architecture

# Overview
BelastingBuddy uses a RAG architecture with document ingestion, chunking, embeddings, retrieval, LLM response generation, and answer citations.

# Components
- Chat UI
- Backend API
- Document ingestion pipeline
- Chunk store / vector database
- LLM runtime
- Logging and feedback storage

# Flow
1. Source documents are collected and normalized.
2. Documents are chunked and embedded.
3. Chunks are stored with metadata.
4. User sends a question.
5. Retriever selects relevant chunks.
6. LLM answers using retrieved context.
7. UI shows answer and citations.
8. Feedback and logs are stored.

# Future additions
- Access control by user type
- Better source freshness checks
- Evaluation dataset
