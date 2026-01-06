"""
Abstract base class for PDF parsers.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from src.models.paper import Paper


class AbstractParser(ABC):
    """
    Base class for all PDF parsers.
    
    Defines the contract that all parser implementations must follow.
    This enables easy swapping between different parsing strategies
    (e.g., Grobid, Nougat, simple PyPDF).
    """

    @abstractmethod
    def parse(self, pdf_path: Path) -> Paper:
        """
        Parse a PDF file and extract structured information.
        
        Args:
            pdf_path: Path to the PDF file to parse
            
        Returns:
            Paper object with extracted metadata and content
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the PDF cannot be parsed
        """
        pass

    def validate_pdf(self, pdf_path: Path) -> None:
        """
        Validate that the file exists and is a PDF.
        
        Args:
            pdf_path: Path to validate
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a PDF
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if pdf_path.suffix.lower() != ".pdf":
            raise ValueError(f"File is not a PDF: {pdf_path}")
