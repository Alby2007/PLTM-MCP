"""
Infectious Atom Tracker - Identifies and tracks self-replicating knowledge patterns.

Measures "infectiousness" of atoms based on:
- Retrieval frequency
- Jury confidence scores
- Cross-domain connectivity
- Survival through conflicts
- Appearance in synthesis suggestions
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from loguru import logger
import math


class InfectiousAtomTracker:
    """
    Tracks and analyzes atoms for memetic fitness - which patterns replicate
    most successfully through the memory system.
    """
    
    def __init__(self, store):
        self.store = store
        self.metrics_cache = {}
    
    async def analyze_infectiousness(
        self,
        min_confidence: float = 0.0,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Analyze all atoms for infectiousness metrics.
        
        Args:
            min_confidence: Minimum confidence threshold
            limit: Limit number of atoms to analyze
            
        Returns:
            List of atoms with infectiousness scores
        """
        if not self.store._conn:
            logger.error("Database not connected")
            return []
        
        # Get all substantiated atoms
        query = """
            SELECT id, subject, predicate, object, confidence, 
                   first_observed, last_accessed, metadata
            FROM atoms 
            WHERE graph = 'substantiated' AND confidence >= ?
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor = await self.store._conn.execute(query, (min_confidence,))
        rows = await cursor.fetchall()
        
        logger.info(f"Analyzing {len(rows)} atoms for infectiousness")
        
        # Calculate metrics for each atom
        results = []
        for row in rows:
            atom_id, subject, predicate, obj, confidence, first_obs, last_acc, metadata_json = row
            
            # Parse metadata
            try:
                metadata = json.loads(metadata_json) if metadata_json else {}
            except:
                metadata = {}
            
            # Calculate infectiousness score
            score = await self._calculate_infectiousness(
                atom_id, subject, predicate, obj, confidence,
                first_obs, last_acc, metadata
            )
            
            results.append({
                'id': atom_id,
                'subject': subject,
                'predicate': predicate,
                'object': obj[:100],  # Truncate for display
                'confidence': confidence,
                'infectiousness_score': score['total'],
                'metrics': score
            })
        
        # Sort by infectiousness score
        results.sort(key=lambda x: x['infectiousness_score'], reverse=True)
        
        logger.info(f"Top infectious atom: {results[0]['predicate']} (score: {results[0]['infectiousness_score']:.3f})")
        
        return results
    
    async def _calculate_infectiousness(
        self,
        atom_id: str,
        subject: str,
        predicate: str,
        obj: str,
        confidence: float,
        first_observed: str,
        last_accessed: str,
        metadata: Dict
    ) -> Dict[str, float]:
        """
        Calculate composite infectiousness score.
        
        Components:
        1. Confidence score (0-1)
        2. Access recency (0-1)
        3. Cross-domain connectivity (0-1)
        4. Predicate rarity (0-1)
        5. Metadata richness (0-1)
        """
        scores = {}
        
        # 1. Confidence score (direct)
        scores['confidence'] = confidence
        
        # 2. Access recency (more recent = more infectious)
        try:
            first_time = datetime.fromisoformat(first_observed)
            last_time = datetime.fromisoformat(last_accessed) if last_accessed else first_time
            now = datetime.now()
            
            # Days since last access
            days_since = (now - last_time).total_seconds() / 86400
            # Decay function: recent access = high score
            scores['recency'] = math.exp(-days_since / 30)  # 30-day half-life
        except:
            scores['recency'] = 0.5
        
        # 3. Cross-domain connectivity (how many related atoms)
        related_count = len(metadata.get('related_atoms', []))
        scores['connectivity'] = min(1.0, related_count / 10)  # Normalize to 0-1
        
        # 4. Predicate rarity (rare predicates are more distinctive)
        cursor = await self.store._conn.execute(
            "SELECT COUNT(*) FROM atoms WHERE predicate = ? AND graph = 'substantiated'",
            (predicate,)
        )
        predicate_count = (await cursor.fetchone())[0]
        
        # Inverse frequency: rare = high score
        cursor = await self.store._conn.execute(
            "SELECT COUNT(*) FROM atoms WHERE graph = 'substantiated'"
        )
        total_atoms = (await cursor.fetchone())[0]
        
        if total_atoms > 0:
            frequency = predicate_count / total_atoms
            # Rare predicates score higher (but not too rare)
            scores['distinctiveness'] = 1.0 - min(frequency * 10, 1.0)
        else:
            scores['distinctiveness'] = 0.5
        
        # 5. Metadata richness (more metadata = more context = more sticky)
        metadata_fields = len(metadata.keys())
        scores['richness'] = min(1.0, metadata_fields / 10)
        
        # Composite score (weighted average)
        weights = {
            'confidence': 0.3,
            'recency': 0.2,
            'connectivity': 0.25,
            'distinctiveness': 0.15,
            'richness': 0.1
        }
        
        total = sum(scores[k] * weights[k] for k in weights.keys())
        scores['total'] = total
        
        return scores
    
    async def export_to_jsonl(
        self,
        output_path: str,
        top_n: int = 100,
        min_score: float = 0.5
    ) -> Dict[str, Any]:
        """
        Export top infectious atoms to JSONL format for fine-tuning.
        
        Args:
            output_path: Path to output JSONL file
            top_n: Number of top atoms to export
            min_score: Minimum infectiousness score
            
        Returns:
            Export statistics
        """
        # Analyze atoms
        results = await self.analyze_infectiousness()
        
        # Filter by score and limit
        infectious = [r for r in results if r['infectiousness_score'] >= min_score][:top_n]
        
        logger.info(f"Exporting {len(infectious)} infectious atoms to {output_path}")
        
        # Format for fine-tuning
        jsonl_data = []
        for atom in infectious:
            # Create training example
            example = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a knowledge system that generates highly memorable, cross-domain insights with strong provenance."
                    },
                    {
                        "role": "user",
                        "content": f"Generate a knowledge claim about: {atom['predicate'].replace('_', ' ')}"
                    },
                    {
                        "role": "assistant",
                        "content": f"{atom['subject']}: {atom['object']}"
                    }
                ],
                "metadata": {
                    "infectiousness_score": atom['infectiousness_score'],
                    "confidence": atom['confidence'],
                    "predicate": atom['predicate'],
                    "metrics": atom['metrics']
                }
            }
            jsonl_data.append(example)
        
        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with output_file.open('w', encoding='utf-8') as f:
            for item in jsonl_data:
                f.write(json.dumps(item) + '\n')
        
        stats = {
            "total_atoms_analyzed": len(results),
            "infectious_atoms_found": len(infectious),
            "exported_to": str(output_path),
            "min_score": min_score,
            "top_n": top_n,
            "avg_infectiousness": sum(a['infectiousness_score'] for a in infectious) / len(infectious) if infectious else 0,
            "avg_confidence": sum(a['confidence'] for a in infectious) / len(infectious) if infectious else 0,
            "top_predicates": self._get_top_predicates(infectious, 5)
        }
        
        logger.info(f"Export complete: {stats['infectious_atoms_found']} atoms exported")
        
        return stats
    
    def _get_top_predicates(self, atoms: List[Dict], n: int) -> List[Dict]:
        """Get top N most common predicates in infectious atoms"""
        predicate_counts = {}
        for atom in atoms:
            pred = atom['predicate']
            predicate_counts[pred] = predicate_counts.get(pred, 0) + 1
        
        sorted_preds = sorted(predicate_counts.items(), key=lambda x: x[1], reverse=True)
        return [{"predicate": p, "count": c} for p, c in sorted_preds[:n]]
    
    async def get_replication_patterns(self) -> Dict[str, Any]:
        """
        Identify patterns in how atoms replicate through the system.
        
        Returns:
            Analysis of replication patterns
        """
        if not self.store._conn:
            return {"error": "Database not connected"}
        
        # Get predicate distribution
        cursor = await self.store._conn.execute("""
            SELECT predicate, COUNT(*) as count, AVG(confidence) as avg_conf
            FROM atoms 
            WHERE graph = 'substantiated'
            GROUP BY predicate
            ORDER BY count DESC
        """)
        predicate_stats = await cursor.fetchall()
        
        # Calculate entropy of predicate distribution
        total = sum(row[1] for row in predicate_stats)
        entropy = 0.0
        for _, count, _ in predicate_stats:
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        
        max_entropy = math.log2(len(predicate_stats)) if len(predicate_stats) > 1 else 1.0
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0
        
        return {
            "total_atoms": total,
            "unique_predicates": len(predicate_stats),
            "entropy": round(entropy, 3),
            "normalized_entropy": round(normalized_entropy, 3),
            "predicate_distribution": [
                {
                    "predicate": row[0],
                    "count": row[1],
                    "avg_confidence": round(row[2], 3),
                    "frequency": round(row[1] / total, 3)
                }
                for row in predicate_stats[:10]
            ],
            "interpretation": self._interpret_entropy(normalized_entropy)
        }
    
    def _interpret_entropy(self, norm_entropy: float) -> str:
        """Interpret what the entropy level means for replication"""
        if norm_entropy < 0.3:
            return "Low diversity - few dominant patterns replicating"
        elif norm_entropy < 0.6:
            return "Moderate diversity - balanced replication"
        elif norm_entropy < 0.8:
            return "High diversity - many patterns competing"
        else:
            return "Maximum diversity - near-uniform distribution"


# Example usage
if __name__ == "__main__":
    import asyncio
    from src.storage.sqlite_store import SQLiteGraphStore
    
    async def test():
        store = SQLiteGraphStore("pltm_mcp.db")
        await store.connect()
        
        tracker = InfectiousAtomTracker(store)
        
        # Analyze infectiousness
        results = await tracker.analyze_infectiousness(limit=20)
        
        print("\nTop 5 Most Infectious Atoms:")
        for i, atom in enumerate(results[:5], 1):
            print(f"\n{i}. [{atom['predicate']}] Score: {atom['infectiousness_score']:.3f}")
            print(f"   Confidence: {atom['confidence']:.2f}")
            print(f"   Object: {atom['object']}")
            print(f"   Metrics: {atom['metrics']}")
        
        # Get replication patterns
        patterns = await tracker.get_replication_patterns()
        print(f"\n\nReplication Patterns:")
        print(f"Total atoms: {patterns['total_atoms']}")
        print(f"Unique predicates: {patterns['unique_predicates']}")
        print(f"Entropy: {patterns['entropy']} ({patterns['interpretation']})")
        
        await store.close()
    
    asyncio.run(test())
