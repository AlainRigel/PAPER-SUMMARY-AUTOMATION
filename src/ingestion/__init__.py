"""
Ingestion module for PDF parsing and paper extraction.
"""

from src.ingestion.base_parser import AbstractParser
from src.ingestion.simple_parser import SimplePDFParser

__all__ = ["AbstractParser", "SimplePDFParser"]
