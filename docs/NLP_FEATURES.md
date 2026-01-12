# NLP Analysis Features

## Overview

The Paper Collector now includes advanced NLP (Natural Language Processing) capabilities for deep academic analysis of scientific papers. These features implement the specifications from `design_specification.md` Section 2.B: **Pipeline de NLP y Extracción de Información**.

## Features

### 1. Scientific Named Entity Recognition (NER)

Extracts domain-specific entities from scientific papers:

- **Task**: Research tasks or problems being addressed
- **Method**: Methodologies, algorithms, or techniques used
- **Metric**: Evaluation metrics (accuracy, F1-score, RMSE, etc.)
- **Material**: Datasets, corpora, or experimental materials
- **Concept**: Key technical concepts and terminology
- **Tool**: Software, hardware, or tools mentioned

**Example:**
```python
from src.analysis import NLPProcessor

nlp = NLPProcessor()
result = nlp.process(paper_text)

for entity in result['entities']:
    print(f"{entity.entity_type}: {entity.text}")
    print(f"  Context: {entity.context}")
```

### 2. Discourse Segmentation

Classifies sentences by their rhetorical function in academic writing:

- **Background**: Prior work and context
- **Objective**: Research goals and aims
- **Method**: Methodological descriptions
- **Result**: Findings and outcomes
- **Conclusion**: Summary and implications
- **Future Work**: Proposed next steps
- **Limitation**: Constraints and challenges

**Example:**
```python
result = nlp.process(abstract_text, section_type="introduction")

for sentence in result['discourse']:
    print(f"[{sentence.function.value}] {sentence.text}")
    print(f"  Confidence: {sentence.confidence:.2f}")
```

### 3. Key Phrase Extraction

Identifies important technical phrases and terminology:

```python
key_phrases = result['key_phrases']

for phrase, score in key_phrases[:10]:
    print(f"{phrase}: {score}")
```

### 4. Scientific Embeddings

Generate semantic embeddings using domain-specific models:

- **SPECTER**: Optimized for scientific paper similarity
- **SciBERT**: BERT trained on scientific corpus
- **MiniLM**: Lightweight general-purpose model

**Example:**
```python
from src.analysis import get_embedder

embedder = get_embedder('specter')
embedding = embedder.embed_paper(
    title="Paper Title",
    abstract="Paper abstract...",
    sections=["Section 1 text...", "Section 2 text..."]
)

# Compute similarity
similarity = embedder.compute_similarity(embedding1, embedding2)
```

### 5. Semantic Search

Build a semantic search engine for your paper collection:

```python
from src.analysis import ScientificEmbedder, SemanticSearchEngine

embedder = ScientificEmbedder('specter')
search_engine = SemanticSearchEngine(embedder)

# Index papers
search_engine.index_paper(
    paper_id="paper1",
    title="Title",
    abstract="Abstract..."
)

# Search
results = search_engine.search("machine learning for speech recognition", top_k=10)

for result in results:
    print(f"{result['title']}: {result['similarity']:.3f}")
```

## Installation

### Basic NLP Features

```bash
pip install spacy nltk
python -m spacy download en_core_web_sm
```

### Embeddings (Optional)

```bash
pip install sentence-transformers
```

### All Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Enhanced Academic Analysis

The `AcademicAnalyzer` now uses NLP by default:

```python
from src.ingestion import SimplePDFParser
from src.analysis import AcademicAnalyzer

# Parse PDF
parser = SimplePDFParser()
paper = parser.parse("path/to/paper.pdf")

# Analyze with NLP
analyzer = AcademicAnalyzer(use_nlp=True)
analysis = analyzer.analyze(paper)

# Access results
print(analysis.main_contributions)
print(analysis.key_concepts)
print(analysis.methodology.techniques)
```

### CLI Usage

```bash
# Run NLP-enhanced analysis
python -m src.analyze path/to/paper.pdf

# Run demo
python examples/nlp_analysis_demo.py path/to/paper.pdf
```

### Web Interface

The web interface (`/api/analyze` endpoint) automatically uses NLP when available.

## NLP Pipeline Architecture

```
Input Text
    ↓
┌─────────────────────────────────┐
│   Text Preprocessing            │
│   - Sentence tokenization       │
│   - Linguistic analysis (spaCy) │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│   Parallel Processing           │
│                                 │
│   ┌─────────────────────────┐  │
│   │ Scientific NER          │  │
│   │ - Pattern matching      │  │
│   │ - Noun phrase extraction│  │
│   └─────────────────────────┘  │
│                                 │
│   ┌─────────────────────────┐  │
│   │ Discourse Segmentation  │  │
│   │ - Keyword indicators    │  │
│   │ - Section context       │  │
│   │ - Position heuristics   │  │
│   └─────────────────────────┘  │
│                                 │
│   ┌─────────────────────────┐  │
│   │ Key Phrase Extraction   │  │
│   │ - Noun chunks           │  │
│   │ - Frequency scoring     │  │
│   └─────────────────────────┘  │
└─────────────────────────────────┘
    ↓
Structured Output
```

## Performance

### Speed

- **NER**: ~100-200 sentences/second
- **Discourse Segmentation**: ~150-250 sentences/second
- **Embeddings**: ~10-50 papers/second (model-dependent)

### Accuracy

Current implementation uses rule-based and pattern-matching approaches:

- **NER Precision**: ~70-80% (domain-dependent)
- **Discourse Classification**: ~60-70% (improves with section context)
- **Key Phrase Relevance**: ~75-85%

**Note**: Future phases will integrate LLMs for higher accuracy.

## Configuration

### Disable NLP

If NLP dependencies are not available or you want to use template-based analysis:

```python
analyzer = AcademicAnalyzer(use_nlp=False)
```

### Choose Embedding Model

```python
# Lightweight (fast, lower accuracy)
embedder = get_embedder('minilm')

# Scientific (slower, higher accuracy)
embedder = get_embedder('specter')

# Best for scientific papers (requires more resources)
embedder = get_embedder('specter2')
```

## Limitations

1. **Language**: Currently only supports English
2. **Domain**: Optimized for STEM papers, may be less accurate for humanities
3. **Accuracy**: Rule-based NER has limitations; LLM integration planned for Phase 3
4. **Resources**: Embedding models require significant memory (1-2GB)

## Future Enhancements (Roadmap)

### Phase 3: LLM Integration
- Replace rule-based extraction with LLM-powered analysis
- Cross-document coreference resolution
- Improved entity linking

### Phase 4: Advanced Features
- Multi-language support
- Fine-tuned models for specific domains
- Real-time analysis streaming
- Citation network analysis

## Examples

See `examples/nlp_analysis_demo.py` for a comprehensive demonstration of all NLP features.

## Troubleshooting

### spaCy Model Not Found

```bash
python -m spacy download en_core_web_sm
```

### NLTK Data Not Found

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### Embedding Model Download Issues

Models are downloaded automatically on first use. Ensure you have:
- Stable internet connection
- Sufficient disk space (~1-2GB per model)
- Write permissions in cache directory

## References

- Design Specification: `design_specification.md`
- spaCy Documentation: https://spacy.io/
- Sentence Transformers: https://www.sbert.net/
- SPECTER: https://github.com/allenai/specter
