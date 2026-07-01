from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "BelastingBuddy API is running"}

@patch("app.main.collection")
def test_health(mock_collection):
    mock_collection.count.return_value = 5
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "collection_count": 5}

@patch("app.main.collection")
def test_ask_empty_collection(mock_collection):
    mock_collection.count.return_value = 0
    response = client.post("/ask", json={"question": "What is the M-form?"})
    assert response.status_code == 200
    assert response.json() == {
        "answer": "Collection is empty. Run python scripts/ingest.py first.",
        "sources": []
    }

@patch("app.main.requests.post")
@patch("app.main.collection")
def test_ask_success(mock_collection, mock_requests_post):
    # 1. Mock ChromaDB collection methods
    mock_collection.count.return_value = 2
    mock_collection.query.return_value = {
        "documents": [["This is chunk 1 content", "This is chunk 2 content"]],
        "metadatas": [[
            {"source_file": "m_form.txt", "chunk_index": 0},
            {"source_file": "m_form.txt", "chunk_index": 1}
        ]]
    }

    # 2. Mock requests.post response from Ollama API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response": "The M-form is for migration. Sources: m_form.txt#chunk-0, m_form.txt#chunk-1"
    }
    mock_requests_post.return_value = mock_response

    # 3. Call endpoint
    response = client.post("/ask", json={"question": "Tell me about the M-form"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["answer"] == "The M-form is for migration. Sources: m_form.txt#chunk-0, m_form.txt#chunk-1"
    assert data["sources"] == ["m_form.txt#chunk-0", "m_form.txt#chunk-1"]

    # 4. Verify query and requests.post were called with correct arguments
    mock_collection.query.assert_called_once_with(
        query_texts=["Tell me about the M-form"],
        n_results=3,
        include=["documents", "metadatas"]
    )
    mock_requests_post.assert_called_once()
    called_args, called_kwargs = mock_requests_post.call_args
    assert called_kwargs["json"]["model"] == "qwen2.5-coder:1.5b"
    assert "Tell me about the M-form" in called_kwargs["json"]["prompt"]
