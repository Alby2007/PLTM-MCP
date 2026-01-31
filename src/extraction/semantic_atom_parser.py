"""
Semantic Atom Parser - Breaks text into atomic semantic units.

Inspired by semantic linebreaks: each atom represents one unit of thought
that corresponds to how LLMs process information via embeddings.
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from loguru import logger


@dataclass
class SemanticUnit:
    """A single atomic unit of meaning"""
    text: str
    unit_type: str  # clause, phrase, concept
    subject: Optional[str] = None
    predicate: Optional[str] = None
    object: Optional[str] = None
    confidence: float = 0.7
    related_units: List[int] = None  # Indices of related units
    
    def __post_init__(self):
        if self.related_units is None:
            self.related_units = []


class SemanticAtomParser:
    """
    Parses text into atomic semantic units aligned with LLM embedding boundaries.
    
    Each unit represents one "thought" - a clause or phrase that forms a
    coherent semantic chunk for vector embedding.
    """
    
    def __init__(self):
        # Patterns for semantic boundaries
        self.clause_markers = [
            r',\s+(?:and|but|or|yet|so|for|nor)\s+',  # Coordinating conjunctions
            r';\s+',  # Semicolons
            r'\.\s+',  # Sentence boundaries
            r',\s+(?:which|that|who|where|when)\s+',  # Relative clauses
            r'\s+(?:because|since|although|while|if|unless|until)\s+',  # Subordinating
        ]
        
        # Patterns for extracting relationships
        self.relation_patterns = [
            (r'(.+?)\s+(?:is|are|was|were)\s+(.+)', 'is_a'),
            (r'(.+?)\s+(?:has|have|had)\s+(.+)', 'has'),
            (r'(.+?)\s+(?:uses|use|used)\s+(.+)', 'uses'),
            (r'(.+?)\s+(?:applies to|applied to)\s+(.+)', 'applies_to'),
            (r'(.+?)\s+(?:extends|extended)\s+(.+)', 'extends'),
            (r'(.+?)\s+(?:proposes|propose|proposed)\s+(.+)', 'proposes'),
            (r'(.+?)\s+(?:shows|show|showed)\s+(.+)', 'shows'),
            (r'(.+?)\s+(?:requires|require|required)\s+(.+)', 'requires'),
        ]
    
    def parse_text(self, text: str) -> List[SemanticUnit]:
        """
        Parse text into atomic semantic units.
        
        Args:
            text: Input text to parse
            
        Returns:
            List of SemanticUnit objects
        """
        # Split into sentences first
        sentences = self._split_sentences(text)
        
        units = []
        for sentence in sentences:
            # Split sentence into clauses
            clauses = self._split_clauses(sentence)
            
            for clause in clauses:
                # Try to extract structured relationship
                unit = self._extract_relationship(clause)
                if unit:
                    units.append(unit)
                else:
                    # Store as unstructured semantic unit
                    units.append(SemanticUnit(
                        text=clause.strip(),
                        unit_type='clause',
                        confidence=0.6
                    ))
        
        # Link related units
        self._link_related_units(units)
        
        logger.debug(f"Parsed {len(units)} semantic units from text")
        return units
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting (can be enhanced with spaCy/nltk)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _split_clauses(self, sentence: str) -> List[str]:
        """Split sentence into clauses at semantic boundaries"""
        clauses = [sentence]
        
        # Apply each clause marker pattern
        for pattern in self.clause_markers:
            new_clauses = []
            for clause in clauses:
                # Split but keep the marker
                parts = re.split(f'({pattern})', clause)
                # Recombine keeping semantic chunks
                current = ""
                for part in parts:
                    if re.match(pattern, part):
                        if current:
                            new_clauses.append(current.strip())
                        current = ""
                    else:
                        current += part
                if current:
                    new_clauses.append(current.strip())
            clauses = new_clauses if new_clauses else clauses
        
        return [c for c in clauses if len(c) > 10]  # Filter very short fragments
    
    def _extract_relationship(self, clause: str) -> Optional[SemanticUnit]:
        """
        Try to extract structured subject-predicate-object from clause.
        
        Returns SemanticUnit if successful, None otherwise.
        """
        clause_clean = clause.strip().rstrip('.,;')
        
        for pattern, predicate in self.relation_patterns:
            match = re.match(pattern, clause_clean, re.IGNORECASE)
            if match:
                subject = match.group(1).strip()
                obj = match.group(2).strip()
                
                return SemanticUnit(
                    text=clause_clean,
                    unit_type='relationship',
                    subject=subject,
                    predicate=predicate,
                    object=obj,
                    confidence=0.8
                )
        
        return None
    
    def _link_related_units(self, units: List[SemanticUnit]):
        """
        Identify and link semantically related units.
        
        Uses simple heuristics:
        - Units with overlapping entities
        - Sequential units (discourse coherence)
        - Units with same subject
        """
        for i, unit in enumerate(units):
            # Link to previous unit (discourse flow)
            if i > 0:
                unit.related_units.append(i - 1)
            
            # Link units with same subject
            if unit.subject:
                for j, other in enumerate(units):
                    if i != j and other.subject == unit.subject:
                        unit.related_units.append(j)
    
    def units_to_atoms(
        self,
        units: List[SemanticUnit],
        source_id: str,
        source_type: str = "arxiv"
    ) -> List[Dict]:
        """
        Convert semantic units to atom format for storage.
        
        Args:
            units: List of SemanticUnit objects
            source_id: Source identifier (e.g., arxiv ID)
            source_type: Type of source
            
        Returns:
            List of atom dictionaries ready for storage
        """
        atoms = []
        
        for i, unit in enumerate(units):
            if unit.subject and unit.predicate and unit.object:
                # Structured relationship atom
                atom = {
                    'subject': 'pltm_knowledge',
                    'predicate': unit.predicate,
                    'object': f"{unit.subject} → {unit.object}",
                    'confidence': unit.confidence,
                    'metadata': {
                        'source_id': source_id,
                        'source_type': source_type,
                        'unit_index': i,
                        'unit_type': unit.unit_type,
                        'full_text': unit.text,
                        'related_units': unit.related_units
                    }
                }
            else:
                # Unstructured semantic unit atom
                atom = {
                    'subject': 'pltm_knowledge',
                    'predicate': 'learned_from_semantic_unit',
                    'object': unit.text,
                    'confidence': unit.confidence,
                    'metadata': {
                        'source_id': source_id,
                        'source_type': source_type,
                        'unit_index': i,
                        'unit_type': unit.unit_type,
                        'related_units': unit.related_units
                    }
                }
            
            atoms.append(atom)
        
        logger.info(f"Converted {len(units)} semantic units to {len(atoms)} atoms")
        return atoms


# Example usage
if __name__ == "__main__":
    parser = SemanticAtomParser()
    
    sample_text = """
    The theory of pattern formation in reaction-diffusion systems is extended 
    to the case of a directed network. We propose a new methodology that uses 
    cellular automata to model complex systems. This approach shows promising 
    results for understanding emergent behavior.
    """
    
    units = parser.parse_text(sample_text)
    
    print(f"\nParsed {len(units)} semantic units:\n")
    for i, unit in enumerate(units):
        print(f"{i+1}. [{unit.unit_type}] {unit.text}")
        if unit.subject:
            print(f"   → {unit.subject} --{unit.predicate}--> {unit.object}")
        if unit.related_units:
            print(f"   Related to units: {unit.related_units}")
        print()
    
    atoms = parser.units_to_atoms(units, "test_paper")
    print(f"\nConverted to {len(atoms)} atoms")
