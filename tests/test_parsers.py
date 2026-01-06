"""
Tests for PDF parsers.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.ingestion.base_parser import AbstractParser
from src.ingestion.simple_parser import SimplePDFParser
from src.models.paper import Paper, SectionType


def test_abstract_parser_validate_pdf_exists(tmp_path: Path) -> None:
    """Test that validate_pdf raises error for non-existent file."""
    
    class DummyParser(AbstractParser):
        def parse(self, pdf_path: Path) -> Paper:
            return Paper(title="Dummy")
    
    parser = DummyParser()
    non_existent = tmp_path / "nonexistent.pdf"
    
    with pytest.raises(FileNotFoundError):
        parser.validate_pdf(non_existent)


def test_abstract_parser_validate_pdf_extension(tmp_path: Path) -> None:
    """Test that validate_pdf raises error for non-PDF file."""
    
    class DummyParser(AbstractParser):
        def parse(self, pdf_path: Path) -> Paper:
            return Paper(title="Dummy")
    
    parser = DummyParser()
    txt_file = tmp_path / "document.txt"
    txt_file.write_text("Not a PDF")
    
    with pytest.raises(ValueError, match="not a PDF"):
        parser.validate_pdf(txt_file)


def test_simple_parser_section_detection() -> None:
    """Test SimplePDFParser section pattern matching."""
    parser = SimplePDFParser()
    
    # Test abstract pattern
    assert parser.SECTION_PATTERNS[SectionType.ABSTRACT]
    
    # Test that patterns are case-insensitive
    import re
    abstract_pattern = parser.SECTION_PATTERNS[SectionType.ABSTRACT]
    assert re.match(abstract_pattern, "Abstract")
    assert re.match(abstract_pattern, "ABSTRACT")
    assert re.match(abstract_pattern, "abstract")


@patch("src.ingestion.simple_parser.PdfReader")
def test_simple_parser_basic_parsing(mock_pdf_reader: MagicMock, tmp_path: Path) -> None:
    """Test SimplePDFParser basic parsing functionality."""
    # Create a mock PDF file
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_bytes(b"%PDF-1.4\nDummy PDF content")
    
    # Mock the PdfReader
    mock_reader_instance = MagicMock()
    mock_pdf_reader.return_value = mock_reader_instance
    
    # Mock metadata
    mock_reader_instance.metadata = {
        "/Title": "Test Paper Title",
        "/Author": "John Doe, Jane Smith"
    }
    
    # Mock pages
    mock_page = MagicMock()
    mock_page.extract_text.return_value = """
    Test Paper Title
    John Doe, Jane Smith
    
    Abstract
    This is the abstract of the paper.
    
    Introduction
    This is the introduction section.
    """
    mock_reader_instance.pages = [mock_page]
    
    # Parse the PDF
    parser = SimplePDFParser()
    paper = parser.parse(pdf_file)
    
    # Assertions
    assert paper.title == "Test Paper Title"
    assert len(paper.authors) == 2
    assert paper.authors[0].name == "John Doe"
    assert paper.authors[1].name == "Jane Smith"
    assert paper.source_file == str(pdf_file)
    assert "simple" in paper.parser_version


def test_simple_parser_extract_title_fallback(tmp_path: Path) -> None:
    """Test that SimplePDFParser falls back to first line if no metadata title."""
    parser = SimplePDFParser()
    
    # Mock reader with no metadata
    mock_reader = MagicMock()
    mock_reader.metadata = None
    
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Fallback Title\nSome content"
    mock_reader.pages = [mock_page]
    
    title = parser._extract_title(mock_reader.metadata, mock_reader)
    assert title == "Fallback Title"
