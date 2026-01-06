"""
Tests for Paper data model.
"""

from datetime import datetime

import pytest

from src.models.paper import Author, Paper, Section, SectionType


def test_author_creation() -> None:
    """Test creating an Author instance."""
    author = Author(
        name="John Doe",
        affiliation="MIT",
        email="john@mit.edu",
        orcid="0000-0001-2345-6789"
    )
    
    assert author.name == "John Doe"
    assert author.affiliation == "MIT"
    assert author.email == "john@mit.edu"
    assert author.orcid == "0000-0001-2345-6789"


def test_author_minimal() -> None:
    """Test creating an Author with only required fields."""
    author = Author(name="Jane Smith")
    
    assert author.name == "Jane Smith"
    assert author.affiliation is None
    assert author.email is None


def test_section_creation() -> None:
    """Test creating a Section instance."""
    section = Section(
        section_type=SectionType.ABSTRACT,
        title="Abstract",
        content="This is the abstract content.",
        page_start=1,
        page_end=1
    )
    
    assert section.section_type == SectionType.ABSTRACT
    assert section.title == "Abstract"
    assert section.content == "This is the abstract content."
    assert section.page_start == 1
    assert section.page_end == 1


def test_paper_creation() -> None:
    """Test creating a Paper instance with full metadata."""
    authors = [
        Author(name="Alice Johnson", affiliation="Stanford"),
        Author(name="Bob Williams", affiliation="Berkeley")
    ]
    
    sections = [
        Section(
            section_type=SectionType.ABSTRACT,
            content="Abstract content here."
        ),
        Section(
            section_type=SectionType.INTRODUCTION,
            title="1. Introduction",
            content="Introduction content here."
        )
    ]
    
    paper = Paper(
        title="A Novel Approach to Machine Learning",
        authors=authors,
        doi="10.1234/example.doi",
        abstract="Abstract content here.",
        sections=sections,
        venue="ICML 2024",
        source_file="/path/to/paper.pdf"
    )
    
    assert paper.title == "A Novel Approach to Machine Learning"
    assert len(paper.authors) == 2
    assert paper.authors[0].name == "Alice Johnson"
    assert paper.doi == "10.1234/example.doi"
    assert len(paper.sections) == 2
    assert paper.venue == "ICML 2024"
    assert isinstance(paper.ingestion_timestamp, datetime)


def test_paper_minimal() -> None:
    """Test creating a Paper with only required fields."""
    paper = Paper(title="Minimal Paper")
    
    assert paper.title == "Minimal Paper"
    assert paper.authors == []
    assert paper.sections == []
    assert paper.references == []
    assert paper.parser_version == "0.1.0"


def test_section_type_enum() -> None:
    """Test SectionType enum values."""
    assert SectionType.ABSTRACT.value == "abstract"
    assert SectionType.METHODOLOGY.value == "methodology"
    assert SectionType.CONCLUSION.value == "conclusion"


def test_paper_json_serialization() -> None:
    """Test that Paper can be serialized to JSON."""
    paper = Paper(
        title="Test Paper",
        authors=[Author(name="Test Author")],
        abstract="Test abstract"
    )
    
    json_data = paper.model_dump_json()
    assert isinstance(json_data, str)
    assert "Test Paper" in json_data
    assert "Test Author" in json_data
