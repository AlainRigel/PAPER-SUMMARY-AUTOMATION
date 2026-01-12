"""
Example: NLP-Enhanced Academic Analysis

This example demonstrates the new NLP capabilities for analyzing scientific papers:
- Scientific Named Entity Recognition (NER)
- Discourse segmentation (rhetorical function classification)
- Key phrase extraction
- Semantic embeddings (optional)

Usage:
    python examples/nlp_analysis_demo.py path/to/paper.pdf
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from src.ingestion import SimplePDFParser
from src.analysis import AcademicAnalyzer, NLP_AVAILABLE, EMBEDDINGS_AVAILABLE

console = Console()


def main():
    """Run NLP analysis demo."""
    
    # Check if PDF path provided
    if len(sys.argv) < 2:
        console.print("[red]Error:[/red] Please provide a PDF file path")
        console.print("\nUsage: python examples/nlp_analysis_demo.py path/to/paper.pdf")
        sys.exit(1)
    
    pdf_path = Path(sys.argv[1])
    
    if not pdf_path.exists():
        console.print(f"[red]Error:[/red] File not found: {pdf_path}")
        sys.exit(1)
    
    # Display capabilities
    console.print("\n[bold cyan]🔬 NLP Analysis Capabilities[/bold cyan]\n")
    
    capabilities_table = Table(show_header=True, header_style="bold magenta")
    capabilities_table.add_column("Feature", style="cyan")
    capabilities_table.add_column("Status", style="green")
    
    capabilities_table.add_row(
        "Scientific NER",
        "✓ Available" if NLP_AVAILABLE else "✗ Not Available (install spacy, nltk)"
    )
    capabilities_table.add_row(
        "Discourse Segmentation",
        "✓ Available" if NLP_AVAILABLE else "✗ Not Available"
    )
    capabilities_table.add_row(
        "Key Phrase Extraction",
        "✓ Available" if NLP_AVAILABLE else "✗ Not Available"
    )
    capabilities_table.add_row(
        "Semantic Embeddings",
        "✓ Available" if EMBEDDINGS_AVAILABLE else "✗ Not Available (install sentence-transformers)"
    )
    
    console.print(capabilities_table)
    console.print()
    
    # Parse PDF
    console.print(f"[bold blue]📄 Analyzing:[/bold blue] {pdf_path.name}\n")
    
    with console.status("[bold green]Parsing PDF..."):
        parser = SimplePDFParser()
        paper = parser.parse(pdf_path)
    
    console.print("[green]✓[/green] PDF parsed successfully\n")
    
    # Perform NLP-enhanced analysis
    with console.status("[bold green]Performing NLP-enhanced analysis..."):
        analyzer = AcademicAnalyzer(use_nlp=True)
        analysis = analyzer.analyze(paper)
    
    console.print("[green]✓[/green] Analysis completed\n")
    
    # Display results
    console.print(Panel.fit(
        f"[bold cyan]{analysis.paper_title}[/bold cyan]",
        title="📚 Academic Analysis",
        border_style="cyan"
    ))
    
    # Show extracted entities
    if NLP_AVAILABLE:
        console.print("\n[bold yellow]🔍 EXTRACTED SCIENTIFIC ENTITIES[/bold yellow]\n")
        
        # Show key concepts
        if analysis.key_concepts:
            concepts_table = Table(show_header=True, header_style="bold magenta")
            concepts_table.add_column("Concept", style="cyan", width=30)
            concepts_table.add_column("Context", width=60)
            
            for concept, context in list(analysis.key_concepts.items())[:10]:
                concepts_table.add_row(concept, context[:100] + "..." if len(context) > 100 else context)
            
            console.print(concepts_table)
            console.print()
    
    # Show methodology analysis
    console.print("\n[bold yellow]⚙️ METHODOLOGY ANALYSIS[/bold yellow]\n")
    
    method_table = Table(show_header=False, box=None)
    method_table.add_row("[cyan]Input Data:[/cyan]", analysis.methodology.input_data)
    method_table.add_row("[cyan]Techniques:[/cyan]", "\n".join(f"• {t}" for t in analysis.methodology.techniques))
    method_table.add_row("[cyan]Evaluation:[/cyan]", analysis.methodology.evaluation)
    
    console.print(method_table)
    
    # Show contributions
    console.print("\n[bold yellow]🎯 MAIN CONTRIBUTIONS[/bold yellow]\n")
    for i, contrib in enumerate(analysis.main_contributions, 1):
        console.print(f"  [green]{i}.[/green] {contrib}")
    
    # Show limitations
    console.print("\n[bold yellow]⚠️ LIMITATIONS[/bold yellow]\n")
    if analysis.limitations:
        for limit in analysis.limitations:
            console.print(f"  [yellow]•[/yellow] {limit}")
    else:
        console.print("  [dim]None explicitly stated[/dim]")
    
    # Show thematic classification
    console.print("\n[bold yellow]🏷️ THEMATIC CLASSIFICATION[/bold yellow]\n")
    console.print("  " + " | ".join(f"[magenta]{tag}[/magenta]" for tag in analysis.thematic_tags))
    
    # Embeddings demo (if available)
    if EMBEDDINGS_AVAILABLE:
        console.print("\n[bold yellow]🧠 SEMANTIC EMBEDDINGS[/bold yellow]\n")
        
        try:
            from src.analysis import get_embedder
            
            with console.status("[bold green]Generating embeddings..."):
                embedder = get_embedder('minilm')  # Use lightweight model for demo
                
                if embedder:
                    embedding = embedder.embed_paper(
                        title=paper.title,
                        abstract=paper.abstract or "",
                        sections=[s.content for s in paper.sections[:2]]
                    )
                    
                    console.print(f"  [cyan]Model:[/cyan] {embedding.model_name}")
                    console.print(f"  [cyan]Dimension:[/cyan] {embedding.dimension}")
                    console.print(f"  [cyan]Embedding shape:[/cyan] {embedding.embedding.shape}")
                    console.print("  [green]✓[/green] Embeddings generated successfully")
        except Exception as e:
            console.print(f"  [yellow]Warning:[/yellow] Could not generate embeddings: {e}")
    
    # Summary
    console.print("\n[bold green]✅ Analysis Complete![/bold green]\n")
    console.print(f"Analysis version: {analyzer.version}")
    console.print(f"NLP enabled: {analyzer.use_nlp}")
    console.print(f"Confidence: {analysis.analysis_confidence}")
    
    if analysis.missing_information:
        console.print(f"\n[yellow]Missing information:[/yellow] {', '.join(analysis.missing_information)}")


if __name__ == "__main__":
    main()
