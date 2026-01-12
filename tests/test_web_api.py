"""
Test script to verify NLP is working in the web API.
This script sends a test PDF to the /api/analyze endpoint.
"""

import sys
from pathlib import Path
import requests
from rich.console import Console
from rich.panel import Panel
from rich.json import JSON
import json

console = Console()


def test_web_api_nlp(pdf_path: str = None, server_url: str = "http://localhost:8000"):
    """
    Test the /api/analyze endpoint with NLP.
    
    Args:
        pdf_path: Path to PDF file to test (optional)
        server_url: URL of the server
    """
    console.print("\n[bold cyan]🌐 Testing Web API NLP Integration[/bold cyan]\n")
    
    # Check if server is running
    console.print(f"[dim]Server URL:[/dim] {server_url}")
    
    try:
        response = requests.get(f"{server_url}/api/health", timeout=5)
        if response.status_code == 200:
            console.print("[green]✓[/green] Server is running\n")
        else:
            console.print("[red]✗[/red] Server returned unexpected status\n")
            return False
    except requests.exceptions.RequestException as e:
        console.print(f"[red]✗[/red] Cannot connect to server: {e}\n")
        console.print("[yellow]Make sure the server is running:[/yellow]")
        console.print("  python app.py\n")
        return False
    
    # If no PDF provided, create a test case
    if not pdf_path:
        console.print("[yellow]⚠[/yellow] No PDF provided. Testing with health check only.\n")
        console.print("[cyan]To test with a real PDF:[/cyan]")
        console.print("  python tests/test_web_api.py path/to/paper.pdf\n")
        return True
    
    pdf_file = Path(pdf_path)
    
    if not pdf_file.exists():
        console.print(f"[red]✗[/red] PDF file not found: {pdf_path}\n")
        return False
    
    console.print(f"[dim]Testing with:[/dim] {pdf_file.name}\n")
    
    # Send PDF to analyze endpoint
    with console.status("[bold green]Uploading and analyzing PDF..."):
        try:
            with open(pdf_file, 'rb') as f:
                files = {'file': (pdf_file.name, f, 'application/pdf')}
                response = requests.post(
                    f"{server_url}/api/analyze",
                    files=files,
                    timeout=60
                )
        except requests.exceptions.RequestException as e:
            console.print(f"[red]✗[/red] Request failed: {e}\n")
            return False
    
    # Check response
    if response.status_code != 200:
        console.print(f"[red]✗[/red] Server returned error: {response.status_code}\n")
        console.print(response.text)
        return False
    
    console.print("[green]✓[/green] Analysis completed\n")
    
    # Parse response
    try:
        data = response.json()
    except json.JSONDecodeError as e:
        console.print(f"[red]✗[/red] Invalid JSON response: {e}\n")
        return False
    
    # Display results
    if not data.get('success'):
        console.print("[red]✗[/red] Analysis failed\n")
        console.print(data)
        return False
    
    console.print(Panel.fit(
        "[bold green]Analysis Successful![/bold green]",
        border_style="green"
    ))
    
    # Show analysis details
    analysis = data.get('analysis', {})
    
    console.print("\n[bold yellow]📊 Analysis Results[/bold yellow]\n")
    
    # Paper info
    console.print(f"[cyan]Title:[/cyan] {analysis.get('paper_title', 'N/A')}")
    console.print(f"[cyan]Analyzer Version:[/cyan] {analysis.get('analysis_confidence', 'N/A')}\n")
    
    # Check for NLP features
    console.print("[bold yellow]🔍 NLP Features Detected[/bold yellow]\n")
    
    # Methodology
    methodology = analysis.get('methodology', {})
    if methodology:
        console.print("[cyan]Methodology:[/cyan]")
        console.print(f"  Input Data: {methodology.get('input_data', 'N/A')}")
        console.print(f"  Techniques: {', '.join(methodology.get('techniques', []))}")
        console.print(f"  Evaluation: {methodology.get('evaluation', 'N/A')}\n")
    
    # Key concepts
    key_concepts = analysis.get('key_concepts', {})
    if key_concepts:
        console.print(f"[cyan]Key Concepts:[/cyan] {len(key_concepts)} found")
        for i, (concept, definition) in enumerate(list(key_concepts.items())[:5], 1):
            console.print(f"  {i}. {concept}")
        if len(key_concepts) > 5:
            console.print(f"  ... and {len(key_concepts) - 5} more\n")
        else:
            console.print()
    
    # Contributions
    contributions = analysis.get('main_contributions', [])
    if contributions:
        console.print(f"[cyan]Main Contributions:[/cyan] {len(contributions)} found")
        for i, contrib in enumerate(contributions, 1):
            console.print(f"  {i}. {contrib[:80]}...")
        console.print()
    
    # Limitations
    limitations = analysis.get('limitations', [])
    if limitations:
        console.print(f"[cyan]Limitations:[/cyan] {len(limitations)} found")
        for i, limit in enumerate(limitations, 1):
            console.print(f"  {i}. {limit[:80]}...")
        console.print()
    
    # Thematic tags
    tags = analysis.get('thematic_tags', [])
    if tags:
        console.print(f"[cyan]Thematic Tags:[/cyan] {', '.join(tags)}\n")
    
    # Check if NLP was actually used
    console.print("[bold yellow]✅ NLP Verification[/bold yellow]\n")
    
    nlp_indicators = []
    
    # Check if techniques were extracted (NLP feature)
    if methodology.get('techniques') and len(methodology['techniques']) > 0:
        if not any('requires' in t.lower() for t in methodology['techniques']):
            nlp_indicators.append("✓ Techniques extracted via NER")
    
    # Check if key concepts were extracted (NLP feature)
    if key_concepts and len(key_concepts) > 1:
        if not all('Requires' in v for v in key_concepts.values()):
            nlp_indicators.append("✓ Key concepts extracted via NLP")
    
    # Check if contributions were extracted (NLP feature)
    if contributions and len(contributions) > 0:
        if not any('requires' in c.lower() for c in contributions):
            nlp_indicators.append("✓ Contributions extracted via discourse analysis")
    
    if nlp_indicators:
        for indicator in nlp_indicators:
            console.print(f"[green]{indicator}[/green]")
        console.print("\n[bold green]🎉 NLP is working in the web API![/bold green]\n")
    else:
        console.print("[yellow]⚠ NLP features not clearly detected[/yellow]")
        console.print("[yellow]This might mean:[/yellow]")
        console.print("  1. NLP dependencies not installed")
        console.print("  2. Server needs to be restarted")
        console.print("  3. PDF content is minimal\n")
    
    # Option to save full response
    console.print("[dim]Full response saved to: test_api_response.json[/dim]")
    with open('test_api_response.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return True


def main():
    """Main entry point."""
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    success = test_web_api_nlp(pdf_path)
    
    if success:
        console.print("[bold green]✅ Test completed successfully[/bold green]\n")
        return 0
    else:
        console.print("[bold red]❌ Test failed[/bold red]\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
