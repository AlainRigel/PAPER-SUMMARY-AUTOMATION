"""
Analysis module for academic paper analysis.

Provides:
- AcademicAnalyzer: Main analysis orchestrator
- NLPProcessor: Scientific NLP processing
- ScientificEmbedder: Embedding generation for semantic search
"""

from src.analysis.academic_analyzer import AcademicAnalyzer, AcademicAnalysis

# Optional NLP components (require additional dependencies)
try:
    from src.analysis.nlp_processor import (
        NLPProcessor,
        ScientificNER,
        DiscourseSegmenter,
        KeyPhraseExtractor,
        RhetoricalFunction,
        ScientificEntityType
    )
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False

# Optional embedding components
try:
    from src.analysis.embeddings import (
        ScientificEmbedder,
        SemanticSearchEngine,
        get_embedder
    )
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False

__all__ = [
    "AcademicAnalyzer",
    "AcademicAnalysis",
    "NLP_AVAILABLE",
    "EMBEDDINGS_AVAILABLE",
]

# Add NLP exports if available
if NLP_AVAILABLE:
    __all__.extend([
        "NLPProcessor",
        "ScientificNER",
        "DiscourseSegmenter",
        "KeyPhraseExtractor",
        "RhetoricalFunction",
        "ScientificEntityType",
    ])

# Add embedding exports if available
if EMBEDDINGS_AVAILABLE:
    __all__.extend([
        "ScientificEmbedder",
        "SemanticSearchEngine",
        "get_embedder",
    ])
