"""
Setup script to download required NLTK data.
Run this after installing dependencies.
"""

import nltk
from rich.console import Console

console = Console()

def download_nltk_data():
    """Download required NLTK datasets."""
    console.print("\n[bold cyan]Downloading NLTK Data...[/bold cyan]\n")
    
    datasets = [
        ('punkt', 'Punkt Tokenizer'),
        ('punkt_tab', 'Punkt Tokenizer Tables'),
        ('stopwords', 'Stopwords'),
        ('averaged_perceptron_tagger', 'POS Tagger'),
    ]
    
    for dataset_id, name in datasets:
        try:
            console.print(f"Downloading {name}...", end=" ")
            nltk.download(dataset_id, quiet=True)
            console.print("[green]✓[/green]")
        except Exception as e:
            console.print(f"[yellow]⚠ {e}[/yellow]")
    
    console.print("\n[green]✓ NLTK data download complete![/green]\n")


if __name__ == "__main__":
    download_nltk_data()
