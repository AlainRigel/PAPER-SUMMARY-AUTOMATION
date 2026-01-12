"""
LLM Integration Module using Groq API.

Groq provides ultra-fast inference with models like Llama and Mixtral.
Much faster than other providers while maintaining high quality.
"""

import os
from typing import Optional, Dict, Any
import json
from groq import Groq


class GroqAnalyzer:
    """
    Analyzer using Groq LLM for intelligent paper analysis.
    
    Groq provides:
    - Ultra-fast inference (10x faster than typical LLMs)
    - High-quality analysis with Llama 3 models
    - Free tier with generous limits
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq analyzer.
        
        Args:
            api_key: Groq API key (or set GROQ_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "Groq API key required. Set GROQ_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Initialize Groq client
        self.client = Groq(api_key=self.api_key)
        
        # Use Llama 3.3 70B - latest stable endpoint
        self.model = "llama-3.3-70b-versatile"
    
    def analyze_paper(self, paper) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of a paper using Groq.
        
        Args:
            paper: Parsed Paper object
            
        Returns:
            Dictionary with analysis results
        """
        # Prepare paper content for analysis
        paper_content = self._prepare_content(paper)
        
        # Create analysis prompt
        prompt = self._create_analysis_prompt(paper_content)
        
        # Call Groq API
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert academic researcher analyzing scientific papers. "
                                   "Provide detailed, accurate analysis in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more focused analysis
                max_tokens=4000,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            analysis_text = response.choices[0].message.content
            analysis = json.loads(analysis_text)
            
            return analysis
            
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return self._get_fallback_analysis()
    
    def _prepare_content(self, paper) -> str:
        """Prepare paper content for LLM analysis."""
        content_parts = []
        
        # Title
        content_parts.append(f"TITLE: {paper.title}")
        
        # Abstract
        if paper.abstract:
            content_parts.append(f"\nABSTRACT:\n{paper.abstract}")
        
        # Sections
        for section in paper.sections:
            if section.section_type.value != "references":  # Skip references
                title = section.title or section.section_type.value.upper()
                # Limit section content to avoid token limits
                content = section.content[:2000] if len(section.content) > 2000 else section.content
                content_parts.append(f"\n{title}:\n{content}")
        
        return "\n".join(content_parts)
    
    def _create_analysis_prompt(self, paper_content: str) -> str:
        """Create the analysis prompt for Groq."""
        return f"""Analyze the following scientific paper and provide a comprehensive academic analysis.

PAPER CONTENT:
{paper_content}

Provide your analysis in JSON format with the following structure:
{{
    "technical_summary": "A 2-3 paragraph formal academic summary of the problem and approach",
    "research_problem": {{
        "problem_statement": "Clear statement of what problem is being solved",
        "domain_relevance": "Why this problem is important in its domain",
        "constraints": ["List of constraints or assumptions"]
    }},
    "methodology": {{
        "input_data": "Description of input data or datasets used",
        "techniques": ["List of algorithms, methods, or techniques used"],
        "pipeline": "Description of the processing pipeline",
        "evaluation": "How the approach is evaluated"
    }},
    "main_contributions": [
        "Contribution 1: Specific, verifiable contribution",
        "Contribution 2: Another concrete contribution",
        "..."
    ],
    "limitations": [
        "Limitation 1: Stated or implied limitation",
        "..."
    ],
    "key_concepts": {{
        "Concept 1": "Definition or explanation",
        "Concept 2": "Definition or explanation",
        "..."
    }},
    "thematic_tags": ["Tag1", "Tag2", "Tag3"],
    "sota_positioning": "How this work positions itself within the state of the art",
    "citation_summary": "A concise paragraph suitable for citing in a literature review",
    "analysis_confidence": "high/medium/low",
    "missing_information": ["List of information not found in the paper"]
}}

Focus on:
1. Extracting concrete, verifiable contributions
2. Identifying actual methodologies and techniques used
3. Finding real limitations stated in the paper
4. Extracting key technical concepts with their definitions
5. Being precise and factual - don't invent information

Respond ONLY with the JSON object, no additional text."""
    
    def _get_fallback_analysis(self) -> Dict[str, Any]:
        """Return fallback analysis if LLM call fails."""
        return {
            "technical_summary": "LLM analysis unavailable. Using fallback mode.",
            "research_problem": {
                "problem_statement": "Unable to extract with LLM",
                "domain_relevance": "Unable to extract with LLM",
                "constraints": []
            },
            "methodology": {
                "input_data": "Unable to extract with LLM",
                "techniques": [],
                "pipeline": "Unable to extract with LLM",
                "evaluation": "Unable to extract with LLM"
            },
            "main_contributions": [
                "LLM analysis failed - please check API key and connection",
                "See server logs for detailed error message"
            ],
            "limitations": [],
            "key_concepts": {},
            "thematic_tags": [],
            "sota_positioning": "Unable to extract with LLM",
            "citation_summary": "Unable to extract with LLM",
            "analysis_confidence": "low",
            "missing_information": ["LLM analysis unavailable"]
        }


def analyze_with_groq(paper, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to analyze a paper with Groq.
    
    Args:
        paper: Parsed Paper object
        api_key: Optional Groq API key
        
    Returns:
        Analysis dictionary
    """
    analyzer = GroqAnalyzer(api_key=api_key)
    return analyzer.analyze_paper(paper)
