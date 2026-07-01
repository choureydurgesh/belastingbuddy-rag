import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts directory to the python path
sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))

from ingest import extract_text_from_pdf

@patch("ingest.PdfReader")
def test_extract_text_from_pdf(mock_pdf_reader):
    # Create mock pages
    page1 = MagicMock()
    page1.extract_text.return_value = "Page 1 of PDF."
    
    page2 = MagicMock()
    page2.extract_text.return_value = "Page 2 of PDF."
    
    # Mock the PdfReader instance
    mock_instance = mock_pdf_reader.return_value
    mock_instance.pages = [page1, page2]
    
    result = extract_text_from_pdf(Path("dummy_path.pdf"))
    
    assert result == "Page 1 of PDF.\nPage 2 of PDF."
    mock_pdf_reader.assert_called_once_with(Path("dummy_path.pdf"))
    page1.extract_text.assert_called_once()
    page2.extract_text.assert_called_once()

@patch("ingest.PdfReader")
def test_extract_text_from_pdf_empty_pages(mock_pdf_reader):
    # Create pages that return None or empty string for extract_text
    page1 = MagicMock()
    page1.extract_text.return_value = None
    
    page2 = MagicMock()
    page2.extract_text.return_value = "  "
    
    mock_instance = mock_pdf_reader.return_value
    mock_instance.pages = [page1, page2]
    
    result = extract_text_from_pdf(Path("dummy_path.pdf"))
    assert result == ""
