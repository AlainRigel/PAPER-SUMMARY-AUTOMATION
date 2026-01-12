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

    # Common section headers in academic papers (Multi-disciplinary)
    # Supports: Engineering, Medicine, Social Sciences, etc.
    SECTION_PATTERNS = {
        SectionType.ABSTRACT: r"(?i)^\s*(?:(?:\d+|[IVX]+)\.?\s*)?(abstract|resumen|summary|executive\s+summary)\s*[:.-]?\s*$",
        
        SectionType.INTRODUCTION: r"(?i)^\s*(?:(?:\d+|[IVX]+)\.?\s*)?(introduction|introducción|background|motivation|overview|preliminaries|problem\s+statement|context)\s*[:.-]?\s*$",
        
        # Engineering & Tech: System Model, Architecture, Proposed Method
        # Medicine: Materials and Methods, Patients and Methods, Clinical Study
        # General: Methodology, Approach
        SectionType.METHODOLOGY: r"(?i)^\s*(?:(?:\d+|[IVX]+)\.?\s*)?(methodology|methods?|materials?\s+and\s+methods?|experimental\s+setup|approach|implementation|system\s+design|architecture|system\s+model|proposed\s+method|algorithm|procedure|study\s+design|participants?|protocol)\s*[:.-]?\s*$",
        
        # Engineering: Performance Evaluation, Simulation Results
        # Medicine: Clinical Outcomes, Findings
        SectionType.RESULTS: r"(?i)^\s*(?:(?:\d+|[IVX]+)\.?\s*)?(results?|findings|experimental\s+results?|experiments?|evaluations?|performance|outcomes?|simulation\s+results?|analysis\s+of\s+results)\s*[:.-]?\s*$",
        
        # Social Sciences: Theoretical Framework, Lit Review often separate but related
        SectionType.DISCUSSION: r"(?i)^\s*(?:(?:\d+|[IVX]+)\.?\s*)?(discussion|analysis|interpretation|limitations?|implications?|theoretical\s+framework|literature\s+review|related\s+work)\s*[:.-]?\s*$",
        
        SectionType.CONCLUSION: r"(?i)^\s*(?:(?:\d+|[IVX]+)\.?\s*)?(conclusion|conclusions|concluding\s+remarks|summary|future\s+work|recommendations?)\s*[:.-]?\s*$",
        
        SectionType.REFERENCES: r"(?i)^\s*(?:(?:\d+|[IVX]+)\.?\s*)?(references?|bibliography|works?\s+cited|sources?)\s*[:.-]?\s*$",
    }

    def parse(self, pdf_path: Path) -> Paper:
        """
        Parse PDF and extract text with basic section detection.
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
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        
        # Attempt to detect sections
        sections = self._detect_sections(full_text)
        
        # Extract abstract if found
        abstract = None
        for section in sections:
            if section.section_type == SectionType.ABSTRACT:
                abstract = section.content
                break
        
        # Fallback: if no sections detected, try to treat first chunk as abstract
        if not abstract and len(sections) > 0 and len(sections[0].content) < 3000:
             # Heuristic: First section often contains abstract if not explicitly labeled
             pass

        return Paper(
            title=title,
            authors=authors,
            abstract=abstract,
            sections=sections,
            source_file=str(pdf_path),
            parser_version="simple-0.2.0-optimized"
        )

    # ... (skipping unchanged metadata methods)

    def _extract_title(self, metadata: dict, reader: PdfReader) -> str:
        """Extract title from metadata or first page."""
        if metadata and metadata.get("/Title"):
            title = str(metadata["/Title"]).strip()
            if title and title.lower() != "untitled":
                return title
        
        # Fallback: use first non-empty line from first page
        if reader.pages:
            try:
                first_page_text = reader.pages[0].extract_text()
                lines = [line.strip() for line in first_page_text.split("\n") if line.strip()]
                if lines:
                    return lines[0]
            except:
                pass
        
        return "Untitled Document"

    def _extract_authors(self, metadata: dict) -> list[Author]:
        """Extract authors from metadata."""
        authors = []
        if metadata and metadata.get("/Author"):
            author_string = str(metadata["/Author"])
            names = re.split(r"[,;]|\sand\s", author_string)
            authors = [Author(name=name.strip()) for name in names if name.strip()]
        return authors

    def _detect_sections(self, text: str) -> list[Section]:
        """
        Attempt to detect sections using pattern matching.
        """
        sections = []
        lines = text.split("\n")
        
        current_section_type = SectionType.OTHER
        current_section_title = None
        current_content = []
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
                
            # Heuristic: Section headers are usually short (< 10 words or < 80 chars)
            is_potential_header = len(line_stripped) < 80 and len(line_stripped.split()) < 10
            
            matched_type = None
            if is_potential_header:
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
                current_content.append(line_stripped)
        
        # Add final section
        if current_content:
            sections.append(Section(
                section_type=current_section_type,
                title=current_section_title,
                content="\n".join(current_content).strip()
            ))
        
        return sections
