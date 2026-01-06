"""
Academic Analysis Module for Paper Collector.

This module provides deep academic analysis of parsed papers,
generating structured outputs suitable for literature reviews,
state-of-the-art sections, and research comparison.
"""

from typing import Optional
from pydantic import BaseModel, Field

from src.models.paper import Paper


class ResearchProblem(BaseModel):
    """Structured representation of the research problem."""
    problem_statement: str = Field(..., description="What problem is being solved")
    domain_relevance: str = Field(..., description="Why it's relevant in its domain")
    constraints: list[str] = Field(default_factory=list, description="Constraints or assumptions")


class Methodology(BaseModel):
    """Structured methodology description."""
    input_data: str = Field(..., description="Input data or signals")
    techniques: list[str] = Field(default_factory=list, description="Algorithms, models, or techniques")
    pipeline: str = Field(..., description="Processing pipeline description")
    evaluation: str = Field(..., description="Evaluation or validation method")


class AcademicAnalysis(BaseModel):
    """
    Complete academic analysis of a scientific paper.
    
    This model represents the structured output of deep analysis,
    suitable for academic use in literature reviews and research comparison.
    """
    
    # Original paper reference
    paper_title: str
    paper_doi: Optional[str] = None
    
    # Section 1: High-level summary
    technical_summary: str = Field(
        ...,
        description="1-2 formal academic paragraphs summarizing problem and approach"
    )
    
    # Section 2: Research problem
    research_problem: ResearchProblem
    
    # Section 3: Methodology
    methodology: Methodology
    
    # Section 4: Main contributions
    main_contributions: list[str] = Field(
        ...,
        min_length=2,
        max_length=5,
        description="2-5 concrete, verifiable contributions"
    )
    
    # Section 5: Limitations
    limitations: list[str] = Field(
        default_factory=list,
        description="Stated or implied limitations and assumptions"
    )
    
    # Section 6: Key concepts
    key_concepts: dict[str, str] = Field(
        default_factory=dict,
        description="Core technical concepts with definitions"
    )
    
    # Section 7: Thematic classification
    thematic_tags: list[str] = Field(
        default_factory=list,
        description="Multi-label academic taxonomy classifications"
    )
    
    # Section 8: State of the art positioning
    sota_positioning: str = Field(
        ...,
        description="Positioning within state of the art"
    )
    
    # Section 9: Citation-ready summary
    citation_summary: str = Field(
        ...,
        description="Concise paragraph for literature review inclusion"
    )
    
    # Metadata
    analysis_confidence: str = Field(
        default="medium",
        description="Confidence level: low, medium, high"
    )
    missing_information: list[str] = Field(
        default_factory=list,
        description="List of information not found in the paper"
    )


class AcademicAnalyzer:
    """
    Analyzer that produces structured academic analysis from parsed papers.
    
    This class will be extended to use LLMs for deep analysis in future phases.
    For now, it provides a structured template and basic extraction.
    """
    
    def __init__(self):
        """Initialize the academic analyzer."""
        self.version = "0.1.0-template"
    
    def analyze(self, paper: Paper) -> AcademicAnalysis:
        """
        Perform academic analysis on a parsed paper.
        
        Args:
            paper: Parsed Paper object
            
        Returns:
            AcademicAnalysis object with structured analysis
            
        Note:
            This is a template implementation. Full LLM-based analysis
            will be implemented in Phase 2.
        """
        # Extract basic information
        abstract = paper.abstract or "Abstract not available"
        
        # Find methodology section
        methodology_content = self._extract_section_content(paper, "methodology")
        introduction_content = self._extract_section_content(paper, "introduction")
        conclusion_content = self._extract_section_content(paper, "conclusion")
        
        # Build analysis (template version)
        analysis = AcademicAnalysis(
            paper_title=paper.title,
            paper_doi=paper.doi,
            
            technical_summary=self._generate_technical_summary(
                paper.title,
                abstract,
                introduction_content
            ),
            
            research_problem=ResearchProblem(
                problem_statement=self._extract_problem_statement(abstract, introduction_content),
                domain_relevance=self._extract_domain_relevance(abstract),
                constraints=self._extract_constraints(methodology_content)
            ),
            
            methodology=Methodology(
                input_data=self._extract_input_data(methodology_content),
                techniques=self._extract_techniques(methodology_content),
                pipeline=self._extract_pipeline(methodology_content),
                evaluation=self._extract_evaluation(methodology_content)
            ),
            
            main_contributions=self._extract_contributions(abstract, conclusion_content),
            
            limitations=self._extract_limitations(conclusion_content),
            
            key_concepts=self._extract_key_concepts(paper),
            
            thematic_tags=self._classify_thematically(paper.title, abstract),
            
            sota_positioning=self._position_in_sota(introduction_content, conclusion_content),
            
            citation_summary=self._generate_citation_summary(
                paper.title,
                abstract,
                conclusion_content
            ),
            
            analysis_confidence="low",  # Template version has low confidence
            missing_information=self._identify_missing_info(paper)
        )
        
        return analysis
    
    def _extract_section_content(self, paper: Paper, section_type: str) -> str:
        """Extract content from a specific section type."""
        for section in paper.sections:
            if section.section_type.value == section_type:
                return section.content
        return ""
    
    def _generate_technical_summary(self, title: str, abstract: str, intro: str) -> str:
        """Generate technical summary (template)."""
        return f"""This paper, titled "{title}", addresses a research problem in its domain. 
        
The proposed approach is described in the abstract and introduction sections. Full analysis requires LLM integration (Phase 2).

[Template Note: This is a placeholder. LLM-based analysis will provide detailed technical summary.]"""
    
    def _extract_problem_statement(self, abstract: str, intro: str) -> str:
        """Extract problem statement."""
        if abstract:
            # Simple heuristic: first sentence often states the problem
            sentences = abstract.split('. ')
            if sentences:
                return sentences[0] + "."
        return "Problem statement not explicitly identified in abstract."
    
    def _extract_domain_relevance(self, abstract: str) -> str:
        """Extract domain relevance."""
        return "Domain relevance requires deeper semantic analysis (Phase 2)."
    
    def _extract_constraints(self, methodology: str) -> list[str]:
        """Extract constraints."""
        if not methodology:
            return ["Methodology section not found"]
        return ["Constraints require LLM-based extraction (Phase 2)"]
    
    def _extract_input_data(self, methodology: str) -> str:
        """Extract input data description."""
        if not methodology:
            return "Not explicitly specified in the paper."
        return "Input data description requires semantic analysis (Phase 2)."
    
    def _extract_techniques(self, methodology: str) -> list[str]:
        """Extract techniques used."""
        if not methodology:
            return ["Not explicitly specified in the paper."]
        return ["Technique extraction requires LLM analysis (Phase 2)"]
    
    def _extract_pipeline(self, methodology: str) -> str:
        """Extract processing pipeline."""
        if not methodology:
            return "Not explicitly specified in the paper."
        return "Pipeline description requires semantic analysis (Phase 2)."
    
    def _extract_evaluation(self, methodology: str) -> str:
        """Extract evaluation method."""
        if not methodology:
            return "Not explicitly specified in the paper."
        return "Evaluation method requires semantic analysis (Phase 2)."
    
    def _extract_contributions(self, abstract: str, conclusion: str) -> list[str]:
        """Extract main contributions."""
        return [
            "Contribution extraction requires LLM-based analysis (Phase 2)",
            "Template placeholder for structured contribution list"
        ]
    
    def _extract_limitations(self, conclusion: str) -> list[str]:
        """Extract limitations."""
        if not conclusion:
            return ["Conclusion section not found"]
        return ["Limitation extraction requires semantic analysis (Phase 2)"]
    
    def _extract_key_concepts(self, paper: Paper) -> dict[str, str]:
        """Extract key concepts."""
        # Simple heuristic: extract capitalized terms
        return {
            "Concept Extraction": "Requires NER and semantic analysis (Phase 2)"
        }
    
    def _classify_thematically(self, title: str, abstract: str) -> list[str]:
        """Classify paper thematically."""
        # Simple keyword-based classification
        tags = []
        text = (title + " " + abstract).lower()
        
        # Basic keyword matching
        if any(word in text for word in ["speech", "voice", "audio"]):
            tags.append("Speech Processing")
        if any(word in text for word in ["recognition", "classification"]):
            tags.append("Pattern Recognition")
        if any(word in text for word in ["embedded", "portable", "device"]):
            tags.append("Embedded Systems")
        if any(word in text for word in ["assistive", "accessibility", "disability"]):
            tags.append("Assistive Technologies")
        if any(word in text for word in ["machine learning", "neural", "deep learning"]):
            tags.append("Machine Learning")
        
        if not tags:
            tags.append("General Research")
        
        return tags
    
    def _position_in_sota(self, intro: str, conclusion: str) -> str:
        """Position within state of the art."""
        return """State-of-the-art positioning requires:
- Analysis of cited prior work
- Identification of research gaps
- Understanding of methodological innovations

Full analysis will be available in Phase 2 with LLM integration."""
    
    def _generate_citation_summary(self, title: str, abstract: str, conclusion: str) -> str:
        """Generate citation-ready summary."""
        return f"""The work titled "{title}" presents a research contribution in its domain. 
The approach and results are described in the paper. 
A detailed citation-ready summary requires LLM-based semantic analysis (Phase 2)."""
    
    def _identify_missing_info(self, paper: Paper) -> list[str]:
        """Identify missing information."""
        missing = []
        
        if not paper.abstract:
            missing.append("Abstract")
        if not paper.doi:
            missing.append("DOI")
        if not paper.authors:
            missing.append("Authors")
        if not paper.publication_date:
            missing.append("Publication date")
        
        # Check for key sections
        section_types = {s.section_type.value for s in paper.sections}
        if "methodology" not in section_types:
            missing.append("Methodology section")
        if "results" not in section_types:
            missing.append("Results section")
        
        return missing
