"""
Command-line interface for Paper Collector.

This CLI provides commands for ingesting, analyzing, and managing academic papers.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from src.ingestion import SimplePDFParser
from src.models.paper import Paper

app = typer.Typer(
    name="paper-collector",
    help="Academic Research Cognitive Amplifier - AI-powered platform for scientific literature analysis",
    add_completion=False,
)
console = Console()


@app.command()
def ingest(
    pdf_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Path to the PDF file to ingest",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output path for JSON file (default: stdout)",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed parsing information",
    ),
) -> None:
    """
    Ingest a PDF paper and extract structured information.
    
    This command parses an academic PDF and extracts:
    - Metadata (title, authors, publication info)
    - Structured sections (abstract, methodology, results, etc.)
    - References
    
    Example:
        paper-collector ingest paper.pdf
        paper-collector ingest paper.pdf -o output.json
    """
    console.print(f"\n[bold blue]📄 Ingesting PDF:[/bold blue] {pdf_path}")
    
    try:
        # Parse the PDF
        parser = SimplePDFParser()
        
        with console.status("[bold green]Parsing PDF..."):
            paper = parser.parse(pdf_path)
        
        console.print("[bold green]✓[/bold green] Parsing completed successfully\n")
        
        # Display summary
        _display_paper_summary(paper, verbose)
        
        # Save to file if requested
        if output:
            output.write_text(paper.model_dump_json(indent=2))
            console.print(f"\n[bold green]✓[/bold green] Saved to: {output}")
        else:
            # Print JSON to stdout
            if verbose:
                console.print("\n[bold]JSON Output:[/bold]")
            json_str = paper.model_dump_json(indent=2)
            syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
            console.print(syntax)
    
    except FileNotFoundError as e:
        console.print(f"[bold red]✗ Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    except ValueError as e:
        console.print(f"[bold red]✗ Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]✗ Unexpected error:[/bold red] {e}")
        if verbose:
            console.print_exception()
        raise typer.Exit(code=1)


def _display_paper_summary(paper: Paper, verbose: bool = False) -> None:
    """Display a formatted summary of the parsed paper."""
    
    # Title panel
    console.print(Panel(
        f"[bold]{paper.title}[/bold]",
        title="📚 Paper Title",
        border_style="blue"
    ))
    
    # Metadata table
    table = Table(title="Metadata", show_header=False, box=None)
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")
    
    if paper.authors:
        authors_str = ", ".join([author.name for author in paper.authors])
        table.add_row("Authors", authors_str)
    
    if paper.doi:
        table.add_row("DOI", paper.doi)
    
    if paper.venue:
        table.add_row("Venue", paper.venue)
    
    table.add_row("Parser", paper.parser_version)
    table.add_row("Sections Found", str(len(paper.sections)))
    
    console.print(table)
    
    # Abstract preview
    if paper.abstract:
        abstract_preview = paper.abstract[:300] + "..." if len(paper.abstract) > 300 else paper.abstract
        console.print(Panel(
            abstract_preview,
            title="📝 Abstract (Preview)",
            border_style="green"
        ))
    
    # Section breakdown
    if verbose and paper.sections:
        console.print("\n[bold]Section Breakdown:[/bold]")
        section_table = Table(show_header=True, header_style="bold magenta")
        section_table.add_column("Type", style="cyan")
        section_table.add_column("Title", style="white")
        section_table.add_column("Length", justify="right", style="yellow")
        
        for section in paper.sections:
            section_table.add_row(
                section.section_type.value,
                section.title or "(no title)",
                f"{len(section.content)} chars"
            )
        
        console.print(section_table)


@app.command()
def version() -> None:
    """Show version information."""
    from src import __version__
    
    console.print(Panel(
        f"[bold]Paper Collector[/bold]\nVersion: {__version__}\n\n"
        "Academic Research Cognitive Amplifier",
        title="ℹ️  Version Info",
        border_style="blue"
    ))


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
