import sys
from pathlib import Path

# Add scripts directory to the python path
sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))

from ingest import chunk_text

def test_chunk_text_empty():
    assert chunk_text("") == []
    assert chunk_text("   ") == []

def test_chunk_text_short():
    text = "Short text"
    chunks = chunk_text(text, chunk_size=50)
    assert chunks == ["Short text"]

def test_chunk_text_exact():
    text = "a" * 50
    chunks = chunk_text(text, chunk_size=50)
    assert chunks == ["a" * 50]

def test_chunk_text_split_no_overlap():
    text = "abcdefghij"
    # chunk size 5, no overlap
    chunks = chunk_text(text, chunk_size=5, overlap=0)
    assert chunks == ["abcde", "fghij"]

def test_chunk_text_split_with_overlap():
    text = "abcdefgh"
    # chunk size 5, overlap 2
    # Chunk 1: indices 0-5 -> "abcde". Next start = end - overlap = 5 - 2 = 3.
    # Chunk 2: indices 3-8 -> "defgh"
    chunks = chunk_text(text, chunk_size=5, overlap=2)
    assert chunks == ["abcde", "defgh"]
