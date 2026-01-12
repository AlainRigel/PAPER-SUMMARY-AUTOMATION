"""
Simple PDF parser implementation using PyPDF.

This is a fallback parser that extracts basic text content.
For production use, prefer Grobid or Nougat for better structure preservation.
"""

import re
from pathlib import Path

from pypdf import PdfReader

from src.ingestion.base_parser import AbstractParser
from src.models.paper import Author, Paper, Section, SectionType


class SimplePDFParser(AbstractParser):
    """
    Basic PDF parser using PyPDF library.
    
    Limitations:
    - Cannot reliably detect section boundaries
    - No metadata extraction from PDF structure
    - Limited handling of multi-column layouts
    
    This parser serves as a baseline and fallback option.
    """

    # Common section headers in academic papers (improved patterns)
    SECTION_PATTERNS = {
        SectionType.ABSTRACT: r"(?i)^(abstract|resumen)\s*$",
        SectionType.INTRODUCTION: r"(?i)^(\d+\.?\s*)?(introduction|introducción|background)\s*$",
        SectionType.METHODOLOGY: r"(?i)^(\d+\.?\s*)?(methodology|methods?|materials?\s+and\s+methods?|experimental\s+setup|approach)\s*$",
        SectionType.RESULTS: r"(?i)^(\d+\.?\s*)?(results?|findings|experimental\s+results?)\s*$",
        SectionType.DISCUSSION: r"(?i)^(\d+\.?\s*)?(discussion|analysis)\s*$",
        SectionType.CONCLUSION: r"(?i)^(\d+\.?\s*)?(conclusion|conclusions|concluding\s+remarks|summary)\s*$",
        SectionType.REFERENCES: r"(?i)^(references?|bibliography|works?\s+cited)\s*$",
    }

    def parse(self, pdf_path: Path) -> Paper:
        """
        Parse PDF and extract text with basic section detection.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Paper object with extracted content
        """
        self.validate_pdf(pdf_path)
        
        reader = PdfReader(str(pdf_path))
        
        # Extract metadata
        metadata = reader.metadata
        title = self._extract_title(metadata, reader)
        authors = self._extract_authors(metadata)
        
        # Extract full text
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        
        # Attempt to detect sections
        sections = self._detect_sections(full_text)
        
        # Extract abstract if found
        abstract = None
        for section in sections:
            if section.section_type == SectionType.ABSTRACT:
                abstract = section.content
                break
        
        return Paper(
            title=title,
            authors=authors,
            abstract=abstract,
            sections=sections,
            source_file=str(pdf_path),
            parser_version="simple-0.1.0"
        )

    def _extract_title(self, metadata: dict, reader: PdfReader) -> str:
        """Extract title from metadata or first page."""
        if metadata and metadata.get("/Title"):
            return str(metadata["/Title"])
        
        # Fallback: use first non-empty line from first page
        if reader.pages:
            first_page_text = reader.pages[0].extract_text()
            lines = [line.strip() for line in first_page_text.split("\n") if line.strip()]
            if lines:
                return lines[0]
        
        return "Untitled Document"

    def _extract_authors(self, metadata: dict) -> list[Author]:
        """Extract authors from metadata."""
        authors = []
        
        if metadata and metadata.get("/Author"):
            author_string = str(metadata["/Author"])
            # Simple split by common delimiters
            names = re.split(r"[,;]|\sand\s", author_string)
            authors = [Author(name=name.strip()) for name in names if name.strip()]
        
        return authors

    def _detect_sections(self, text: str) -> list[Section]:
        """
        Attempt to detect sections using pattern matching.
        
        This is a heuristic approach and may not work for all papers.
        """
        sections = []
        lines = text.split("\n")
        
        current_section_type = SectionType.OTHER
        current_section_title = None
        current_content = []
        
        for line in lines:
            line_stripped = line.strip()
            
            # Check if this line is a section header
            matched_type = None
            for section_type, pattern in self.SECTION_PATTERNS.items():
                if re.match(pattern, line_stripped):
                    matched_type = section_type
                    break
            
            if matched_type:
                # Save previous section if exists
                if current_content:
                    sections.append(Section(
                        section_type=current_section_type,
                        title=current_section_title,
                        content="\n".join(current_content).strip()
                    ))
                
                # Start new section
                current_section_type = matched_type
                current_section_title = line_stripped
                current_content = []
            else:
                # Add to current section
                if line_stripped:
                    current_content.append(line_stripped)
        
        # Add final section
        if current_content:
            sections.append(Section(
                section_type=current_section_type,
                title=current_section_title,
                content="\n".join(current_content).strip()
            ))
        
        return sections
