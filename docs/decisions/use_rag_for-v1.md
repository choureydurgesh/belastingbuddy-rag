# ADR 0001: Use RAG for v1

# Status
Accepted

# Context
BelastingBuddy needs to answer tax-filing questions from trusted guidance while minimizing hallucinations.

# Decision
Use retrieval-augmented generation (RAG) for version 1 instead of fine-tuning a model.

# Consequences
- Faster to implement
- Easier to update when tax guidance changes
- Better answer traceability through citations
- Requires a good ingestion and retrieval pipeline
