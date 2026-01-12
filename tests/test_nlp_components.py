"""
Quick test script to verify NLP components are working.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.panel import Panel

console = Console()

def test_nlp_imports():
    """Test that NLP components can be imported."""
    console.print("\n[bold cyan]Testing NLP Imports...[/bold cyan]\n")
    
    try:
        from src.analysis import NLP_AVAILABLE, EMBEDDINGS_AVAILABLE
        console.print(f"✓ NLP Available: {NLP_AVAILABLE}")
        console.print(f"✓ Embeddings Available: {EMBEDDINGS_AVAILABLE}")
        
        if NLP_AVAILABLE:
            from src.analysis import (
                NLPProcessor,
                ScientificNER,
                DiscourseSegmenter,
                KeyPhraseExtractor
            )
            console.print("✓ All NLP components imported successfully")
        else:
            console.print("[yellow]⚠ NLP components not available[/yellow]")
            return False
        
        return True
    except Exception as e:
        console.print(f"[red]✗ Import error: {e}[/red]")
        return False


def test_nlp_processing():
    """Test NLP processing on sample text."""
    console.print("\n[bold cyan]Testing NLP Processing...[/bold cyan]\n")
    
    try:
        from src.analysis import NLPProcessor
        
        # Sample scientific text
        sample_text = """
        This paper presents a novel approach to speech recognition using deep learning.
        We propose a convolutional neural network architecture for acoustic modeling.
        The system achieves 95% accuracy on the TIMIT dataset.
        However, the model requires significant computational resources.
        Future work will explore more efficient architectures.
        """
        
        console.print("[dim]Sample text:[/dim]")
        console.print(Panel(sample_text.strip(), border_style="dim"))
        
        # Initialize processor
        with console.status("[bold green]Initializing NLP processor..."):
            nlp = NLPProcessor()
        
        console.print("✓ NLP processor initialized\n")
        
        # Process text
        with console.status("[bold green]Processing text..."):
            result = nlp.process(sample_text)
        
        console.print("✓ Text processed\n")
        
        # Display results
        console.print(f"[cyan]Entities found:[/cyan] {len(result['entities'])}")
        for entity in result['entities'][:5]:
            console.print(f"  • [{entity.entity_type.value}] {entity.text}")
        
        console.print(f"\n[cyan]Sentences segmented:[/cyan] {len(result['discourse'])}")
        for sent in result['discourse'][:3]:
            console.print(f"  • [{sent.function.value}] {sent.text[:60]}...")
        
        console.print(f"\n[cyan]Key phrases:[/cyan] {len(result['key_phrases'])}")
        for phrase, score in result['key_phrases'][:5]:
            console.print(f"  • {phrase} ({score:.1f})")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Processing error: {e}[/red]")
        import traceback
        traceback.print_exc()
        return False


def test_academic_analyzer():
    """Test academic analyzer with NLP."""
    console.print("\n[bold cyan]Testing Academic Analyzer...[/bold cyan]\n")
    
    try:
        from src.analysis import AcademicAnalyzer
        from src.models.paper import Paper, Section, SectionType
        
        # Create a mock paper
        paper = Paper(
            title="Deep Learning for Speech Recognition",
            abstract="This paper presents a novel deep learning approach for automatic speech recognition. We propose a CNN-based architecture that achieves state-of-the-art results.",
            sections=[
                Section(
                    section_type=SectionType.METHODOLOGY,
                    content="We use a convolutional neural network with 5 layers. The model is trained on the TIMIT dataset using cross-entropy loss."
                ),
                Section(
                    section_type=SectionType.RESULTS,
                    content="Our approach achieves 95% accuracy on the test set, outperforming previous methods by 3%."
                ),
                Section(
                    section_type=SectionType.CONCLUSION,
                    content="We presented a novel CNN architecture for speech recognition. However, the model requires significant GPU resources. Future work will explore model compression."
                )
            ]
        )
        
        # Analyze with NLP
        with console.status("[bold green]Analyzing paper..."):
            analyzer = AcademicAnalyzer(use_nlp=True)
            analysis = analyzer.analyze(paper)
        
        console.print("✓ Analysis completed\n")
        
        # Display results
        console.print(f"[cyan]Analyzer version:[/cyan] {analyzer.version}")
        console.print(f"[cyan]NLP enabled:[/cyan] {analyzer.use_nlp}")
        console.print(f"[cyan]Confidence:[/cyan] {analysis.analysis_confidence}\n")
        
        console.print("[cyan]Extracted techniques:[/cyan]")
        for tech in analysis.methodology.techniques:
            console.print(f"  • {tech}")
        
        console.print(f"\n[cyan]Key concepts:[/cyan]")
        for concept, definition in list(analysis.key_concepts.items())[:3]:
            console.print(f"  • {concept}")
        
        console.print(f"\n[cyan]Contributions:[/cyan]")
        for contrib in analysis.main_contributions:
            console.print(f"  • {contrib[:80]}...")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Analyzer error: {e}[/red]")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    console.print(Panel.fit(
        "[bold cyan]NLP Components Test Suite[/bold cyan]",
        border_style="cyan"
    ))
    
    results = []
    
    # Test imports
    results.append(("Imports", test_nlp_imports()))
    
    # Test NLP processing
    if results[0][1]:  # Only if imports succeeded
        results.append(("NLP Processing", test_nlp_processing()))
        results.append(("Academic Analyzer", test_academic_analyzer()))
    
    # Summary
    console.print("\n" + "="*60)
    console.print("[bold cyan]Test Summary[/bold cyan]\n")
    
    for test_name, passed in results:
        status = "[green]✓ PASSED[/green]" if passed else "[red]✗ FAILED[/red]"
        console.print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        console.print("\n[bold green]🎉 All tests passed![/bold green]")
    else:
        console.print("\n[bold red]❌ Some tests failed[/bold red]")
    
    console.print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
