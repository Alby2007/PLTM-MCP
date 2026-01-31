"""
Domain Taxonomy - Hierarchical Knowledge Organization

Organizes predicates into a hierarchical taxonomy for:
- Better retrieval (query parent domains)
- Entropy calculation (domain diversity)
- Knowledge gaps identification
- Cross-domain synthesis

Example hierarchy:
  knowledge
    ├── scientific
    │   ├── physics
    │   │   ├── quantum_mechanics
    │   │   └── thermodynamics
    │   └── biology
    └── social
        ├── psychology
        └── economics
"""

from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json

from loguru import logger


@dataclass
class TaxonomyNode:
    """Node in the domain taxonomy tree"""
    domain: str
    parent: Optional[str] = None
    children: Set[str] = field(default_factory=set)
    predicates: Set[str] = field(default_factory=set)
    description: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "domain": self.domain,
            "parent": self.parent,
            "children": list(self.children),
            "predicates": list(self.predicates),
            "description": self.description
        }


class DomainTaxonomy:
    """
    Hierarchical taxonomy for organizing knowledge domains.
    
    Features:
    - Auto-classify predicates into domains
    - Navigate hierarchy (parent/child/sibling)
    - Find knowledge gaps (sparse domains)
    - Cross-domain synthesis opportunities
    """
    
    def __init__(self, store=None):
        self.store = store
        self.nodes: Dict[str, TaxonomyNode] = {}
        self.predicate_to_domain: Dict[str, str] = {}
        
        # Initialize with base taxonomy
        self._initialize_base_taxonomy()
        
        logger.info("DomainTaxonomy initialized")
    
    def _initialize_base_taxonomy(self):
        """Create base taxonomy structure"""
        
        # Root
        self.add_domain("root", description="Root of all knowledge")
        
        # Top-level domains
        self.add_domain("knowledge", parent="root", description="Factual knowledge")
        self.add_domain("personality", parent="root", description="User traits and preferences")
        self.add_domain("meta", parent="root", description="Self-knowledge and improvement")
        
        # Knowledge subdomains
        self.add_domain("scientific", parent="knowledge", description="Scientific knowledge")
        self.add_domain("technical", parent="knowledge", description="Technical skills")
        self.add_domain("social", parent="knowledge", description="Social sciences")
        self.add_domain("creative", parent="knowledge", description="Arts and creativity")
        
        # Scientific subdomains
        self.add_domain("physics", parent="scientific", description="Physics and cosmology")
        self.add_domain("biology", parent="scientific", description="Life sciences")
        self.add_domain("chemistry", parent="scientific", description="Chemical sciences")
        self.add_domain("mathematics", parent="scientific", description="Mathematical sciences")
        
        # Technical subdomains
        self.add_domain("programming", parent="technical", description="Software development")
        self.add_domain("engineering", parent="technical", description="Engineering disciplines")
        self.add_domain("data_science", parent="technical", description="Data and ML")
        
        # Social subdomains
        self.add_domain("psychology", parent="social", description="Human behavior")
        self.add_domain("economics", parent="social", description="Economic systems")
        self.add_domain("politics", parent="social", description="Political systems")
        
        # Personality subdomains
        self.add_domain("preferences", parent="personality", description="User preferences")
        self.add_domain("traits", parent="personality", description="Personality traits")
        self.add_domain("mood", parent="personality", description="Emotional states")
        self.add_domain("communication", parent="personality", description="Communication style")
        
        # Meta subdomains
        self.add_domain("self_improvement", parent="meta", description="System improvements")
        self.add_domain("criticality", parent="meta", description="Criticality monitoring")
        self.add_domain("efficiency", parent="meta", description="Performance metrics")
        
        logger.info(f"Initialized base taxonomy with {len(self.nodes)} domains")
    
    def add_domain(
        self,
        domain: str,
        parent: Optional[str] = None,
        description: str = ""
    ) -> TaxonomyNode:
        """Add a domain to the taxonomy"""
        
        if domain in self.nodes:
            logger.warning(f"Domain {domain} already exists")
            return self.nodes[domain]
        
        node = TaxonomyNode(
            domain=domain,
            parent=parent,
            description=description
        )
        
        self.nodes[domain] = node
        
        # Update parent's children
        if parent and parent in self.nodes:
            self.nodes[parent].children.add(domain)
        
        logger.debug(f"Added domain: {domain} (parent: {parent})")
        return node
    
    def classify_predicate(self, predicate: str) -> str:
        """
        Classify a predicate into a domain.
        
        Uses keyword matching and patterns.
        """
        
        # Check if already classified
        if predicate in self.predicate_to_domain:
            return self.predicate_to_domain[predicate]
        
        pred_lower = predicate.lower()
        
        # Personality patterns
        if any(k in pred_lower for k in ["prefers", "likes", "dislikes", "favorite"]):
            domain = "preferences"
        elif any(k in pred_lower for k in ["is_feeling", "mood", "emotion"]):
            domain = "mood"
        elif any(k in pred_lower for k in ["has_trait", "personality", "characteristic"]):
            domain = "traits"
        elif any(k in pred_lower for k in ["communication", "speaks", "writes"]):
            domain = "communication"
        
        # Knowledge patterns
        elif any(k in pred_lower for k in ["learned_from", "knows_about", "studied"]):
            domain = "knowledge"
        elif any(k in pred_lower for k in ["physics", "quantum", "relativity"]):
            domain = "physics"
        elif any(k in pred_lower for k in ["biology", "genetics", "evolution"]):
            domain = "biology"
        elif any(k in pred_lower for k in ["programming", "code", "software"]):
            domain = "programming"
        elif any(k in pred_lower for k in ["math", "equation", "theorem"]):
            domain = "mathematics"
        elif any(k in pred_lower for k in ["psychology", "cognitive", "behavior"]):
            domain = "psychology"
        
        # Meta patterns
        elif any(k in pred_lower for k in ["applied_improvement", "hypothesis"]):
            domain = "self_improvement"
        elif any(k in pred_lower for k in ["criticality", "entropy", "integration"]):
            domain = "criticality"
        elif any(k in pred_lower for k in ["efficiency", "aae", "performance"]):
            domain = "efficiency"
        
        # Default to knowledge
        else:
            domain = "knowledge"
        
        # Store classification
        self.predicate_to_domain[predicate] = domain
        
        # Add predicate to domain node
        if domain in self.nodes:
            self.nodes[domain].predicates.add(predicate)
        
        return domain
    
    def get_path_to_root(self, domain: str) -> List[str]:
        """Get path from domain to root"""
        path = []
        current = domain
        
        while current and current in self.nodes:
            path.append(current)
            current = self.nodes[current].parent
        
        return path
    
    def get_siblings(self, domain: str) -> List[str]:
        """Get sibling domains (same parent)"""
        if domain not in self.nodes:
            return []
        
        parent = self.nodes[domain].parent
        if not parent or parent not in self.nodes:
            return []
        
        siblings = list(self.nodes[parent].children)
        siblings.remove(domain)
        return siblings
    
    def get_descendants(self, domain: str) -> Set[str]:
        """Get all descendant domains (recursive)"""
        if domain not in self.nodes:
            return set()
        
        descendants = set()
        to_visit = list(self.nodes[domain].children)
        
        while to_visit:
            child = to_visit.pop()
            descendants.add(child)
            if child in self.nodes:
                to_visit.extend(self.nodes[child].children)
        
        return descendants
    
    def find_knowledge_gaps(self, min_predicates: int = 3) -> List[Tuple[str, int]]:
        """
        Find domains with few predicates (knowledge gaps).
        
        Returns list of (domain, predicate_count) sorted by count.
        """
        gaps = []
        
        for domain, node in self.nodes.items():
            if domain == "root":
                continue
            
            count = len(node.predicates)
            if count < min_predicates:
                gaps.append((domain, count))
        
        gaps.sort(key=lambda x: x[1])
        return gaps
    
    def suggest_cross_domain_synthesis(self) -> List[Tuple[str, str, str]]:
        """
        Suggest cross-domain synthesis opportunities.
        
        Returns list of (domain1, domain2, reason).
        """
        suggestions = []
        
        # Find domains with many predicates
        rich_domains = [
            (d, len(n.predicates))
            for d, n in self.nodes.items()
            if len(n.predicates) >= 5
        ]
        rich_domains.sort(key=lambda x: x[1], reverse=True)
        
        # Suggest combinations of non-sibling domains
        for i, (d1, c1) in enumerate(rich_domains[:5]):
            for d2, c2 in rich_domains[i+1:6]:
                # Skip if siblings (too similar)
                if d2 in self.get_siblings(d1):
                    continue
                
                # Skip if parent-child (too hierarchical)
                if d2 in self.get_descendants(d1):
                    continue
                if d1 in self.get_descendants(d2):
                    continue
                
                reason = f"Rich domains ({c1} + {c2} predicates) from different branches"
                suggestions.append((d1, d2, reason))
        
        return suggestions[:5]
    
    def get_domain_stats(self) -> Dict[str, any]:
        """Get taxonomy statistics"""
        
        total_domains = len(self.nodes)
        total_predicates = len(self.predicate_to_domain)
        
        # Depth distribution
        depths = {}
        for domain in self.nodes:
            depth = len(self.get_path_to_root(domain)) - 1
            depths[depth] = depths.get(depth, 0) + 1
        
        # Predicate distribution
        pred_counts = [len(n.predicates) for n in self.nodes.values()]
        avg_predicates = sum(pred_counts) / len(pred_counts) if pred_counts else 0
        
        return {
            "total_domains": total_domains,
            "total_predicates": total_predicates,
            "max_depth": max(depths.keys()) if depths else 0,
            "avg_predicates_per_domain": round(avg_predicates, 2),
            "depth_distribution": depths
        }
    
    async def build_from_atoms(self, user_id: Optional[str] = None, limit: Optional[int] = None):
        """
        Build taxonomy from existing atoms in database.
        
        Classifies all predicates and updates domain nodes.
        """
        if not self.store or not self.store._conn:
            logger.warning("No database connection - cannot build from atoms")
            return
        
        # Get all predicates with optional limit
        if user_id:
            if limit:
                cursor = await self.store._conn.execute(
                    "SELECT DISTINCT predicate FROM atoms WHERE subject = ? LIMIT ?",
                    (user_id, limit)
                )
            else:
                cursor = await self.store._conn.execute(
                    "SELECT DISTINCT predicate FROM atoms WHERE subject = ?",
                    (user_id,)
                )
        else:
            if limit:
                cursor = await self.store._conn.execute(
                    "SELECT DISTINCT predicate FROM atoms LIMIT ?",
                    (limit,)
                )
            else:
                cursor = await self.store._conn.execute(
                    "SELECT DISTINCT predicate FROM atoms"
                )
        
        rows = await cursor.fetchall()
        predicates = [r[0] for r in rows]
        
        # Classify each predicate
        classified = 0
        for pred in predicates:
            self.classify_predicate(pred)
            classified += 1
            
            # Log progress every 50 predicates
            if classified % 50 == 0:
                logger.debug(f"Classified {classified}/{len(predicates)} predicates")
        
        logger.info(f"Built taxonomy from {len(predicates)} predicates across {len(self.nodes)} domains")
    
    def export_taxonomy(self) -> Dict:
        """Export taxonomy as JSON-serializable dict"""
        return {
            "nodes": {d: n.to_dict() for d, n in self.nodes.items()},
            "predicate_map": self.predicate_to_domain,
            "stats": self.get_domain_stats()
        }
    
    def import_taxonomy(self, data: Dict):
        """Import taxonomy from exported dict"""
        self.nodes.clear()
        self.predicate_to_domain.clear()
        
        # Import nodes
        for domain, node_data in data.get("nodes", {}).items():
            node = TaxonomyNode(
                domain=node_data["domain"],
                parent=node_data.get("parent"),
                children=set(node_data.get("children", [])),
                predicates=set(node_data.get("predicates", [])),
                description=node_data.get("description", "")
            )
            self.nodes[domain] = node
        
        # Import predicate map
        self.predicate_to_domain = data.get("predicate_map", {})
        
        logger.info(f"Imported taxonomy with {len(self.nodes)} domains")
