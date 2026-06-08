# project ->> belastingbuddy-rag

BelastingBuddy is an AI assistant for Dutch income tax filling guidance.It helps users understand
filing steps, required documents, deadlines, and special cases using trusted knowledge sources and grounded answers.

# Problem
Many users struggle to understand Dutch tax filing steps, especially when dealing with forms, migration-year filing, and required documents.

# Solution
BelastingBuddy uses retrieval-augmented generation (RAG) to answer user questions from curated tax guidance and project-managed knowledge sources.

# Scope
- Income tax return guidance
- Required documents checklist
- Filing steps and navigation help
- Migration-year filing guidance
- Cited answers

# Architecture
- Chat UI
- Retrieval layer
- Vector store
- LLM backend
- Document ingestion pipeline
- Logging and feedback

# Documentation
See the `docs/` folder for PRD, architecture, risks, and testing.

