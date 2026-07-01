# ADR 0002: Fully Local Deployment Stack

## Status
Accepted

## Context
BelastingBuddy handles sensitive financial and personal query context. To protect user privacy, minimize operations/hosting cost, and make development simple, we need a deployment stack that can run offline.

## Decision
Deploy the entire prototype stack locally using:
1. **Ollama**: To serve open source LLMs (specifically `qwen2.5-coder:1.5b`) on the local CPU/GPU.
2. **ChromaDB**: As an embedded, persistent file-based vector database stored in [vectorstore/](file:///Users/durgeshchourey/Documents/rag-project/belastingbuddy-rag/vectorstore/).
3. **FastAPI**: As a local backend API server.

## Consequences
* **Privacy**: Sensitive tax queries never leave the user's local machine.
* **Cost**: $0 operational cost for hosting vector databases and LLM APIs.
* **Offline Capable**: The application runs without an internet connection once model files are downloaded.
* **Resource Limits**: The performance and speed of answers depend on the local machine's specs.
