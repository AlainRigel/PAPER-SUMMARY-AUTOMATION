"""
Scientific Embeddings Module.

This module provides embedding generation for scientific papers using
domain-specific models like SciBERT and SPECTER2.

Based on design_specification.md Section 2.A: Modelos de Representación (Embeddings)
"""

from typing import List, Optional, Union
import numpy as np
from dataclasses import dataclass

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available. Install with: pip install sentence-transformers")


@dataclass
class EmbeddingResult:
    """Result of embedding generation."""
    embedding: np.ndarray
    model_name: str
    dimension: int


class ScientificEmbedder:
    """
    Scientific paper embedding generator.
    
    Uses domain-specific models trained on scientific literature:
    - allenai/specter2: Optimized for scientific paper similarity
    - allenai/scibert: BERT trained on scientific corpus
    
    These models capture semantic relationships better than generic models
    for academic content.
    """
    
    # Available models
    MODELS = {
        'specter2': 'allenai/specter2',
        'scibert': 'sentence-transformers/allenai-scibert_scivocab_uncased',
        'specter': 'sentence-transformers/allenai-specter',
        'minilm': 'sentence-transformers/all-MiniLM-L6-v2',  # Fallback lightweight model
    }
    
    def __init__(self, model_name: str = 'specter'):
        """
        Initialize the scientific embedder.
        
        Args:
            model_name: Name of the model to use ('specter2', 'scibert', 'specter', 'minilm')
        
        Raises:
            ImportError: If sentence-transformers is not installed
            ValueError: If model_name is not recognized
        """
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "sentence-transformers is required for embeddings. "
                "Install with: pip install sentence-transformers"
            )
        
        if model_name not in self.MODELS:
            raise ValueError(
                f"Unknown model: {model_name}. "
                f"Available models: {list(self.MODELS.keys())}"
            )
        
        self.model_name = model_name
        self.model_path = self.MODELS[model_name]
        
        # Load model (will download on first use)
        print(f"Loading embedding model: {self.model_path}")
        self.model = SentenceTransformer(self.model_path)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        print(f"✓ Model loaded. Embedding dimension: {self.dimension}")
    
    def embed_text(self, text: Union[str, List[str]]) -> Union[EmbeddingResult, List[EmbeddingResult]]:
        """
        Generate embeddings for text.
        
        Args:
            text: Single text string or list of texts
            
        Returns:
            EmbeddingResult or list of EmbeddingResult objects
        """
        is_single = isinstance(text, str)
        texts = [text] if is_single else text
        
        # Generate embeddings
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=len(texts) > 10
        )
        
        # Wrap in result objects
        results = [
            EmbeddingResult(
                embedding=emb,
                model_name=self.model_name,
                dimension=self.dimension
            )
            for emb in embeddings
        ]
        
        return results[0] if is_single else results
    
    def embed_paper(
        self,
        title: str,
        abstract: str,
        sections: Optional[List[str]] = None
    ) -> EmbeddingResult:
        """
        Generate embedding for a complete paper.
        
        For scientific papers, we combine title and abstract as they contain
        the most concentrated semantic information.
        
        Args:
            title: Paper title
            abstract: Paper abstract
            sections: Optional list of section texts to include
            
        Returns:
            EmbeddingResult for the paper
        """
        # Combine title and abstract (weighted)
        # Title is more important for topic identification
        paper_text = f"{title}. {title}. {abstract}"
        
        # Optionally include key sections
        if sections:
            # Limit to avoid token limits
            sections_text = " ".join(sections[:3])[:1000]
            paper_text += f" {sections_text}"
        
        return self.embed_text(paper_text)
    
    def compute_similarity(
        self,
        embedding1: Union[np.ndarray, EmbeddingResult],
        embedding2: Union[np.ndarray, EmbeddingResult]
    ) -> float:
        """
        Compute cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding (array or EmbeddingResult)
            embedding2: Second embedding (array or EmbeddingResult)
            
        Returns:
            Similarity score between 0 and 1
        """
        # Extract arrays if EmbeddingResult objects
        if isinstance(embedding1, EmbeddingResult):
            embedding1 = embedding1.embedding
        if isinstance(embedding2, EmbeddingResult):
            embedding2 = embedding2.embedding
        
        # Compute cosine similarity
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        
        # Ensure in [0, 1] range
        return float(np.clip((similarity + 1) / 2, 0, 1))


class SemanticSearchEngine:
    """
    Semantic search engine for scientific papers.
    
    Uses embeddings to find semantically similar papers or passages.
    """
    
    def __init__(self, embedder: ScientificEmbedder):
        """
        Initialize the search engine.
        
        Args:
            embedder: ScientificEmbedder instance to use
        """
        self.embedder = embedder
        self.paper_embeddings = []
        self.paper_metadata = []
    
    def index_paper(
        self,
        paper_id: str,
        title: str,
        abstract: str,
        sections: Optional[List[str]] = None
    ):
        """
        Index a paper for semantic search.
        
        Args:
            paper_id: Unique identifier for the paper
            title: Paper title
            abstract: Paper abstract
            sections: Optional section texts
        """
        embedding = self.embedder.embed_paper(title, abstract, sections)
        
        self.paper_embeddings.append(embedding.embedding)
        self.paper_metadata.append({
            'id': paper_id,
            'title': title,
            'abstract': abstract
        })
    
    def search(
        self,
        query: str,
        top_k: int = 10
    ) -> List[dict]:
        """
        Search for papers semantically similar to a query.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            
        Returns:
            List of result dictionaries with paper metadata and similarity scores
        """
        if not self.paper_embeddings:
            return []
        
        # Embed query
        query_embedding = self.embedder.embed_text(query).embedding
        
        # Compute similarities
        similarities = []
        for i, paper_emb in enumerate(self.paper_embeddings):
            sim = self.embedder.compute_similarity(query_embedding, paper_emb)
            similarities.append((i, sim))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-k results
        results = []
        for idx, sim in similarities[:top_k]:
            result = self.paper_metadata[idx].copy()
            result['similarity'] = sim
            results.append(result)
        
        return results


# Convenience function for quick embedding generation
def get_embedder(model: str = 'specter') -> Optional[ScientificEmbedder]:
    """
    Get a scientific embedder instance.
    
    Args:
        model: Model name to use
        
    Returns:
        ScientificEmbedder instance or None if dependencies not available
    """
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        print("Warning: sentence-transformers not installed. Embeddings not available.")
        return None
    
    try:
        return ScientificEmbedder(model)
    except Exception as e:
        print(f"Error loading embedder: {e}")
        return None
