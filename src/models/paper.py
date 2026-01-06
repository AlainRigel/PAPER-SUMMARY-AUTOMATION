"""
Data models for academic papers and their components.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class SectionType(str, Enum):
    """Types of sections in an academic paper."""

    ABSTRACT = "abstract"
    INTRODUCTION = "introduction"
    BACKGROUND = "background"
    METHODOLOGY = "methodology"
    RESULTS = "results"
    DISCUSSION = "discussion"
    CONCLUSION = "conclusion"
    REFERENCES = "references"
    ACKNOWLEDGMENTS = "acknowledgments"
    APPENDIX = "appendix"
    OTHER = "other"


class Author(BaseModel):
    """Represents an author of a paper."""

    name: str = Field(..., description="Full name of the author")
    affiliation: Optional[str] = Field(None, description="Institutional affiliation")
    email: Optional[str] = Field(None, description="Contact email")
    orcid: Optional[str] = Field(None, description="ORCID identifier")


class Section(BaseModel):
    """Represents a section within a paper."""

    section_type: SectionType = Field(..., description="Type of section")
    title: Optional[str] = Field(None, description="Section title")
    content: str = Field(..., description="Full text content of the section")
    page_start: Optional[int] = Field(None, description="Starting page number")
    page_end: Optional[int] = Field(None, description="Ending page number")


class Paper(BaseModel):
    """
    Core data model representing an academic paper.
    
    This model captures both metadata and structured content,
    enabling downstream AI processing and analysis.
    """

    # Identifiers
    doi: Optional[str] = Field(None, description="Digital Object Identifier")
    arxiv_id: Optional[str] = Field(None, description="arXiv identifier")
    pubmed_id: Optional[str] = Field(None, description="PubMed ID")
    
    # Bibliographic metadata
    title: str = Field(..., description="Paper title")
    authors: list[Author] = Field(default_factory=list, description="List of authors")
    publication_date: Optional[datetime] = Field(None, description="Publication date")
    venue: Optional[str] = Field(None, description="Journal or conference name")
    
    # Content
    abstract: Optional[str] = Field(None, description="Paper abstract")
    sections: list[Section] = Field(default_factory=list, description="Structured sections")
    
    # References
    references: list[str] = Field(
        default_factory=list, 
        description="List of cited references (raw strings)"
    )
    
    # Processing metadata
    source_file: Optional[str] = Field(None, description="Path to source PDF")
    ingestion_timestamp: datetime = Field(
        default_factory=lambda: datetime.utcnow(),
        description="When this paper was ingested"
    )
    parser_version: str = Field(default="0.1.0", description="Version of parser used")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "title": "Attention Is All You Need",
                "authors": [
                    {"name": "Ashish Vaswani", "affiliation": "Google Brain"}
                ],
                "abstract": "The dominant sequence transduction models...",
                "doi": "10.48550/arXiv.1706.03762"
            }
        }
