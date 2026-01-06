"""
CLI command for academic analysis of papers.

Usage:
    python -m src.analyze path/to/paper.pdf
"""

import sys
from pathlib import Path
import json

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table

from src.ingestion import SimplePDFParser
from src.analysis import AcademicAnalyzer

console = Console()


def format_analysis_output(analysis):
    """Format academic analysis for terminal display."""
    
    console.print("\n")
    console.print(Panel.fit(
        f"[bold cyan]{analysis.paper_title}[/bold cyan]",
        title="📚 Academic Analysis",
        border_style="cyan"
    ))
    
    # Section 1: Technical Summary
    console.print("\n[bold]1. HIGH-LEVEL TECHNICAL SUMMARY[/bold]", style="yellow")
    console.print(Panel(analysis.technical_summary, border_style="dim"))
    
    # Section 2: Research Problem
    console.print("\n[bold]2. RESEARCH PROBLEM DEFINITION[/bold]", style="yellow")
    table = Table(show_header=False, box=None)
    table.add_row("[cyan]Problem:[/cyan]", analysis.research_problem.problem_statement)
    table.add_row("[cyan]Relevance:[/cyan]", analysis.research_problem.domain_relevance)
    if analysis.research_problem.constraints:
        table.add_row("[cyan]Constraints:[/cyan]", "\n".join(f"• {c}" for c in analysis.research_problem.constraints))
    console.print(table)
    
    # Section 3: Methodology
    console.print("\n[bold]3. METHODOLOGY[/bold]", style="yellow")
    method_table = Table(show_header=False, box=None)
    method_table.add_row("[cyan]Input Data:[/cyan]", analysis.methodology.input_data)
    method_table.add_row("[cyan]Techniques:[/cyan]", "\n".join(f"• {t}" for t in analysis.methodology.techniques))
    method_table.add_row("[cyan]Pipeline:[/cyan]", analysis.methodology.pipeline)
    method_table.add_row("[cyan]Evaluation:[/cyan]", analysis.methodology.evaluation)
    console.print(method_table)
    
    # Section 4: Main Contributions
    console.print("\n[bold]4. MAIN CONTRIBUTIONS[/bold]", style="yellow")
    for i, contrib in enumerate(analysis.main_contributions, 1):
        console.print(f"  [green]{i}.[/green] {contrib}")
    
    # Section 5: Limitations
    console.print("\n[bold]5. LIMITATIONS AND ASSUMPTIONS[/bold]", style="yellow")
    if analysis.limitations:
        for limit in analysis.limitations:
            console.print(f"  [yellow]•[/yellow] {limit}")
    else:
        console.print("  [dim]None explicitly stated[/dim]")
    
    # Section 6: Key Concepts
    console.print("\n[bold]6. KEY CONCEPTS AND TERMINOLOGY[/bold]", style="yellow")
    concept_table = Table(show_header=True, header_style="bold magenta")
    concept_table.add_column("Concept", style="cyan")
    concept_table.add_column("Definition")
    for concept, definition in analysis.key_concepts.items():
        concept_table.add_row(concept, definition)
    console.print(concept_table)
    
    # Section 7: Thematic Classification
    console.print("\n[bold]7. THEMATIC CLASSIFICATION[/bold]", style="yellow")
    console.print("  " + " | ".join(f"[magenta]{tag}[/magenta]" for tag in analysis.thematic_tags))
    
    # Section 8: SOTA Positioning
    console.print("\n[bold]8. POSITIONING WITHIN STATE OF THE ART[/bold]", style="yellow")
    console.print(Panel(analysis.sota_positioning, border_style="dim"))
    
    # Section 9: Citation-Ready Summary
    console.print("\n[bold]9. CITATION-READY SUMMARY[/bold]", style="yellow")
    console.print(Panel(analysis.citation_summary, border_style="green"))
    
    # Metadata
    console.print("\n[bold]ANALYSIS METADATA[/bold]", style="dim")
    meta_table = Table(show_header=False, box=None)
    meta_table.add_row("Confidence:", analysis.analysis_confidence)
    if analysis.missing_information:
        meta_table.add_row("Missing Info:", ", ".join(analysis.missing_information))
    console.print(meta_table)


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        console.print("[red]Error:[/red] Please provide a PDF file path")
        console.print("\nUsage: python -m src.analyze path/to/paper.pdf")
        console.print("       python -m src.analyze path/to/paper.pdf --json output.json")
        sys.exit(1)
    
    pdf_path = Path(sys.argv[1])
    
    if not pdf_path.exists():
        console.print(f"[red]Error:[/red] File not found: {pdf_path}")
        sys.exit(1)
    
    if not pdf_path.suffix.lower() == '.pdf':
        console.print(f"[red]Error:[/red] File must be a PDF")
        sys.exit(1)
    
    # Check for JSON output option
    json_output = None
    if len(sys.argv) > 3 and sys.argv[2] == '--json':
        json_output = Path(sys.argv[3])
    
    console.print(f"\n[bold blue]📄 Analyzing:[/bold blue] {pdf_path.name}")
    
    try:
        # Parse PDF
        with console.status("[bold green]Parsing PDF..."):
            parser = SimplePDFParser()
            paper = parser.parse(pdf_path)
        
        console.print("[green]✓[/green] PDF parsed successfully")
        
        # Perform academic analysis
        with console.status("[bold green]Performing academic analysis..."):
            analyzer = AcademicAnalyzer()
            analysis = analyzer.analyze(paper)
        
        console.print("[green]✓[/green] Analysis completed")
        
        # Display results
        format_analysis_output(analysis)
        
        # Save JSON if requested
        if json_output:
            output_data = {
                "paper": paper.model_dump(mode='json'),
                "analysis": analysis.model_dump(mode='json')
            }
            json_output.write_text(json.dumps(output_data, indent=2), encoding='utf-8')
            console.print(f"\n[green]✓[/green] Saved to: {json_output}")
    
    except Exception as e:
        console.print(f"\n[red]✗ Error:[/red] {e}")
        if "--debug" in sys.argv:
            console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()
