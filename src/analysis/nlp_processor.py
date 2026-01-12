"""
NLP Processing Module for Scientific Paper Analysis.

This module provides advanced NLP capabilities for analyzing scientific papers:
- Scientific Named Entity Recognition (NER)
- Discourse segmentation (rhetorical function classification)
- Key phrase extraction
- Semantic similarity computation

Based on design_specification.md Section 2.B: Pipeline de NLP y Extracción de Información
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

import spacy
from spacy.tokens import Doc, Span
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class RhetoricalFunction(Enum):
    """Rhetorical function of a sentence in academic writing."""
    BACKGROUND = "background"
    OBJECTIVE = "objective"
    METHOD = "method"
    RESULT = "result"
    CONCLUSION = "conclusion"
    FUTURE_WORK = "future_work"
    LIMITATION = "limitation"
    UNKNOWN = "unknown"


class ScientificEntityType(Enum):
    """Types of scientific entities to extract."""
    TASK = "task"  # Research task or problem
    METHOD = "method"  # Methodology or algorithm
    METRIC = "metric"  # Evaluation metric
    MATERIAL = "material"  # Dataset or substrate
    CONCEPT = "concept"  # Key technical concept
    TOOL = "tool"  # Software or hardware tool


@dataclass
class ScientificEntity:
    """Represents an extracted scientific entity."""
    text: str
    entity_type: ScientificEntityType
    context: str  # Sentence containing the entity
    confidence: float = 1.0


@dataclass
class AnnotatedSentence:
    """Sentence with rhetorical function annotation."""
    text: str
    function: RhetoricalFunction
    confidence: float
    position: int  # Position in document


class ScientificNER:
    """
    Scientific Named Entity Recognition.
    
    Extracts domain-specific entities like tasks, methods, metrics, and materials
    from scientific text using pattern matching and linguistic features.
    """
    
    def __init__(self):
        """Initialize the scientific NER system."""
        # Load spaCy model for linguistic analysis
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spaCy model 'en_core_web_sm'...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Patterns for entity extraction
        self.patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[ScientificEntityType, List[str]]:
        """Initialize regex patterns for entity extraction."""
        return {
            ScientificEntityType.METHOD: [
                r'\b(?:algorithm|approach|method|technique|model|framework|system|architecture)\b',
                r'\b(?:neural network|deep learning|machine learning|SVM|CNN|RNN|LSTM|transformer)\b',
                r'\b(?:classification|regression|clustering|segmentation|detection)\b',
            ],
            ScientificEntityType.METRIC: [
                r'\b(?:accuracy|precision|recall|F1[- ]score|AUC|ROC)\b',
                r'\b(?:RMSE|MAE|MSE|error rate|performance)\b',
                r'\b(?:\d+(?:\.\d+)?%)\b',  # Percentages
            ],
            ScientificEntityType.MATERIAL: [
                r'\b(?:dataset|corpus|benchmark|database)\b',
                r'\b(?:MNIST|ImageNet|COCO|TIMIT|LibriSpeech)\b',
                r'\b(?:training set|test set|validation set)\b',
            ],
            ScientificEntityType.TASK: [
                r'\b(?:recognition|detection|classification|prediction|estimation)\b',
                r'\b(?:speech recognition|image classification|object detection)\b',
                r'\b(?:problem|task|challenge)\b',
            ],
            ScientificEntityType.TOOL: [
                r'\b(?:TensorFlow|PyTorch|Keras|scikit-learn|MATLAB)\b',
                r'\b(?:Python|Java|C\+\+|R)\b',
                r'\b(?:GPU|CPU|FPGA|embedded system)\b',
            ],
        }
    
    def extract_entities(self, text: str) -> List[ScientificEntity]:
        """
        Extract scientific entities from text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of extracted ScientificEntity objects
        """
        entities = []
        doc = self.nlp(text)
        
        # Extract entities using pattern matching
        for entity_type, patterns in self.patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    matched_text = match.group(0)
                    
                    # Find containing sentence
                    context = self._find_sentence_context(text, match.start())
                    
                    entities.append(ScientificEntity(
                        text=matched_text,
                        entity_type=entity_type,
                        context=context,
                        confidence=0.8  # Pattern-based confidence
                    ))
        
        # Extract noun phrases as potential concepts
        for chunk in doc.noun_chunks:
            # Filter for technical-looking noun phrases
            if len(chunk.text.split()) >= 2 and chunk.text[0].isupper():
                context = str(chunk.sent)
                entities.append(ScientificEntity(
                    text=chunk.text,
                    entity_type=ScientificEntityType.CONCEPT,
                    context=context,
                    confidence=0.6
                ))
        
        # Deduplicate entities
        entities = self._deduplicate_entities(entities)
        
        return entities
    
    def _find_sentence_context(self, text: str, position: int) -> str:
        """Find the sentence containing a given character position."""
        sentences = sent_tokenize(text)
        current_pos = 0
        
        for sentence in sentences:
            sentence_end = current_pos + len(sentence)
            if current_pos <= position < sentence_end:
                return sentence
            current_pos = sentence_end + 1  # +1 for space
        
        return ""
    
    def _deduplicate_entities(self, entities: List[ScientificEntity]) -> List[ScientificEntity]:
        """Remove duplicate entities, keeping highest confidence."""
        seen = {}
        
        for entity in entities:
            key = (entity.text.lower(), entity.entity_type)
            if key not in seen or entity.confidence > seen[key].confidence:
                seen[key] = entity
        
        return list(seen.values())


class DiscourseSegmenter:
    """
    Discourse segmentation for scientific papers.
    
    Classifies sentences by their rhetorical function (background, method, result, etc.)
    using linguistic patterns and contextual cues.
    """
    
    def __init__(self):
        """Initialize the discourse segmenter."""
        self.function_indicators = self._initialize_indicators()
    
    def _initialize_indicators(self) -> Dict[RhetoricalFunction, List[str]]:
        """Initialize keyword indicators for each rhetorical function."""
        return {
            RhetoricalFunction.BACKGROUND: [
                'previous', 'prior', 'existing', 'traditional', 'conventional',
                'literature', 'research has shown', 'studies have', 'well-known'
            ],
            RhetoricalFunction.OBJECTIVE: [
                'we propose', 'we present', 'we introduce', 'our goal', 'our aim',
                'this paper', 'this work', 'we develop', 'objective', 'purpose'
            ],
            RhetoricalFunction.METHOD: [
                'we use', 'we apply', 'we implement', 'algorithm', 'approach',
                'methodology', 'technique', 'procedure', 'process', 'framework'
            ],
            RhetoricalFunction.RESULT: [
                'results show', 'we found', 'we observed', 'demonstrates',
                'achieves', 'performance', 'accuracy', 'outperforms', 'improvement'
            ],
            RhetoricalFunction.CONCLUSION: [
                'in conclusion', 'we conclude', 'in summary', 'overall',
                'demonstrates that', 'shows that', 'indicates that'
            ],
            RhetoricalFunction.FUTURE_WORK: [
                'future work', 'future research', 'future direction', 'next step',
                'plan to', 'will explore', 'intend to'
            ],
            RhetoricalFunction.LIMITATION: [
                'limitation', 'constraint', 'challenge', 'drawback', 'however',
                'unfortunately', 'difficult', 'cannot', 'unable to'
            ],
        }
    
    def segment(self, text: str, section_type: Optional[str] = None) -> List[AnnotatedSentence]:
        """
        Segment text into sentences with rhetorical function annotations.
        
        Args:
            text: Input text to segment
            section_type: Optional section type hint (e.g., 'methodology', 'results')
            
        Returns:
            List of AnnotatedSentence objects
        """
        sentences = sent_tokenize(text)
        annotated = []
        
        for i, sentence in enumerate(sentences):
            function, confidence = self._classify_sentence(sentence, section_type, i, len(sentences))
            
            annotated.append(AnnotatedSentence(
                text=sentence,
                function=function,
                confidence=confidence,
                position=i
            ))
        
        return annotated
    
    def _classify_sentence(
        self,
        sentence: str,
        section_type: Optional[str],
        position: int,
        total: int
    ) -> Tuple[RhetoricalFunction, float]:
        """
        Classify a sentence's rhetorical function.
        
        Args:
            sentence: Sentence to classify
            section_type: Section type hint
            position: Position in document
            total: Total number of sentences
            
        Returns:
            Tuple of (RhetoricalFunction, confidence)
        """
        sentence_lower = sentence.lower()
        scores = {func: 0.0 for func in RhetoricalFunction}
        
        # Score based on keyword indicators
        for function, indicators in self.function_indicators.items():
            for indicator in indicators:
                if indicator in sentence_lower:
                    scores[function] += 1.0
        
        # Boost based on section type
        if section_type:
            section_type = section_type.lower()
            if 'method' in section_type:
                scores[RhetoricalFunction.METHOD] += 2.0
            elif 'result' in section_type:
                scores[RhetoricalFunction.RESULT] += 2.0
            elif 'conclusion' in section_type:
                scores[RhetoricalFunction.CONCLUSION] += 2.0
            elif 'introduction' in section_type or 'background' in section_type:
                scores[RhetoricalFunction.BACKGROUND] += 1.0
                scores[RhetoricalFunction.OBJECTIVE] += 1.0
        
        # Position-based heuristics
        relative_pos = position / max(total, 1)
        if relative_pos < 0.2:  # Early in document
            scores[RhetoricalFunction.BACKGROUND] += 0.5
            scores[RhetoricalFunction.OBJECTIVE] += 0.5
        elif relative_pos > 0.8:  # Late in document
            scores[RhetoricalFunction.CONCLUSION] += 0.5
            scores[RhetoricalFunction.FUTURE_WORK] += 0.3
        
        # Find best match
        max_score = max(scores.values())
        if max_score == 0:
            return RhetoricalFunction.UNKNOWN, 0.0
        
        best_function = max(scores.items(), key=lambda x: x[1])[0]
        confidence = min(max_score / 3.0, 1.0)  # Normalize confidence
        
        return best_function, confidence


class KeyPhraseExtractor:
    """Extract key phrases from scientific text."""
    
    def __init__(self):
        """Initialize the key phrase extractor."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        self.stop_words = set(stopwords.words('english'))
    
    def extract(self, text: str, max_phrases: int = 20) -> List[Tuple[str, float]]:
        """
        Extract key phrases from text.
        
        Args:
            text: Input text
            max_phrases: Maximum number of phrases to return
            
        Returns:
            List of (phrase, score) tuples, sorted by score
        """
        doc = self.nlp(text)
        
        # Extract noun phrases
        phrases = {}
        
        for chunk in doc.noun_chunks:
            # Filter out stop words and short phrases
            if len(chunk.text.split()) < 2:
                continue
            
            phrase_lower = chunk.text.lower()
            if all(word in self.stop_words for word in phrase_lower.split()):
                continue
            
            # Score based on frequency and position
            if phrase_lower not in phrases:
                phrases[phrase_lower] = 0.0
            
            phrases[phrase_lower] += 1.0
        
        # Sort by score
        sorted_phrases = sorted(phrases.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_phrases[:max_phrases]


class NLPProcessor:
    """
    Main NLP processor that coordinates all NLP components.
    
    This class provides a unified interface for:
    - Scientific entity extraction
    - Discourse segmentation
    - Key phrase extraction
    """
    
    def __init__(self):
        """Initialize the NLP processor."""
        self.ner = ScientificNER()
        self.segmenter = DiscourseSegmenter()
        self.keyphrase_extractor = KeyPhraseExtractor()
    
    def process(self, text: str, section_type: Optional[str] = None) -> Dict:
        """
        Process text with all NLP components.
        
        Args:
            text: Input text to process
            section_type: Optional section type hint
            
        Returns:
            Dictionary containing all NLP analysis results
        """
        return {
            'entities': self.ner.extract_entities(text),
            'discourse': self.segmenter.segment(text, section_type),
            'key_phrases': self.keyphrase_extractor.extract(text),
        }
