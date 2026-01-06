"""
Example script demonstrating programmatic usage of Paper Collector.

This script shows how to use the library directly in Python code,
rather than through the CLI.
"""

from pathlib import Path

from src.ingestion import SimplePDFParser
from src.models.paper import SectionType


def main() -> None:
    """Demonstrate basic usage of the Paper Collector library."""
    
    # Initialize parser
    parser = SimplePDFParser()
    
    # Example: Parse a PDF file
    pdf_path = Path("data/sample.pdf")
    
    if not pdf_path.exists():
        print(f"Sample PDF not found at {pdf_path}")
        print("Please place a PDF file at data/sample.pdf to run this example.")
        return
    
    print(f"Parsing: {pdf_path}")
    paper = parser.parse(pdf_path)
    
    # Access paper metadata
    print(f"\nTitle: {paper.title}")
    print(f"Authors: {', '.join([author.name for author in paper.authors])}")
    print(f"Number of sections: {len(paper.sections)}")
    
    # Find specific sections
    abstract = next(
        (s for s in paper.sections if s.section_type == SectionType.ABSTRACT),
        None
    )
    
    if abstract:
        print(f"\nAbstract found ({len(abstract.content)} characters)")
        print(f"Preview: {abstract.content[:200]}...")
    
    # Export to JSON
    output_path = Path("data/parsed_paper.json")
    output_path.write_text(paper.model_dump_json(indent=2))
    print(f"\nSaved to: {output_path}")
    
    # Example: Filter sections by type
    methodology_sections = [
        s for s in paper.sections 
        if s.section_type == SectionType.METHODOLOGY
    ]
    
    print(f"\nMethodology sections found: {len(methodology_sections)}")
    
    # Example: Access raw data as dictionary
    paper_dict = paper.model_dump()
    print(f"\nPaper as dict has {len(paper_dict)} top-level keys")


if __name__ == "__main__":
    main()
