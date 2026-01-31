"""
Prepare Infectious Atom Training Data

Creates 3 datasets for fine-tuning experiment:
1. Control: Random sample of atoms
2. Infectious: Top infectious atoms by memetic fitness
3. Balanced: Mix of infectious and random

Run this to generate JSONL files for fine-tuning.
"""

import asyncio
import json
from pathlib import Path
from src.storage.sqlite_store import SQLiteGraphStore
from src.analysis.infectious_tracker import InfectiousAtomTracker
from loguru import logger


async def prepare_datasets():
    """Prepare all three training datasets"""
    
    # Connect to database
    db_path = Path(__file__).parent / "pltm_mcp.db"
    store = SQLiteGraphStore(str(db_path))
    await store.connect()
    
    logger.info(f"Connected to database: {db_path}")
    
    # Initialize tracker
    tracker = InfectiousAtomTracker(store)
    
    # Analyze all atoms
    logger.info("Analyzing atoms for infectiousness...")
    results = await tracker.analyze_infectiousness()
    
    total_atoms = len(results)
    logger.info(f"Analyzed {total_atoms} atoms")
    
    if total_atoms == 0:
        logger.error("No atoms found in database!")
        return
    
    # Calculate dataset sizes (aim for ~100 examples each)
    dataset_size = min(100, total_atoms // 3)
    
    logger.info(f"Creating datasets with {dataset_size} examples each")
    
    # === DATASET 1: CONTROL (Random Sample) ===
    logger.info("\n=== Creating Control Dataset ===")
    control_atoms = results[::len(results)//dataset_size][:dataset_size]  # Evenly spaced sample
    
    control_data = []
    for atom in control_atoms:
        example = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a knowledge system that stores and retrieves information."
                },
                {
                    "role": "user",
                    "content": f"What do you know about: {atom['predicate'].replace('_', ' ')}"
                },
                {
                    "role": "assistant",
                    "content": atom['object']
                }
            ],
            "metadata": {
                "dataset": "control",
                "confidence": atom['confidence'],
                "predicate": atom['predicate']
            }
        }
        control_data.append(example)
    
    control_path = Path("datasets/control_atoms.jsonl")
    control_path.parent.mkdir(exist_ok=True)
    
    with control_path.open('w', encoding='utf-8') as f:
        for item in control_data:
            f.write(json.dumps(item) + '\n')
    
    logger.info(f"✓ Control dataset: {len(control_data)} examples → {control_path}")
    
    # === DATASET 2: INFECTIOUS (Top Memetic Fitness) ===
    logger.info("\n=== Creating Infectious Dataset ===")
    infectious_atoms = results[:dataset_size]  # Top N by infectiousness score
    
    infectious_data = []
    for atom in infectious_atoms:
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
                    "content": atom['object']
                }
            ],
            "metadata": {
                "dataset": "infectious",
                "infectiousness_score": atom['infectiousness_score'],
                "confidence": atom['confidence'],
                "predicate": atom['predicate'],
                "metrics": atom['metrics']
            }
        }
        infectious_data.append(example)
    
    infectious_path = Path("datasets/infectious_atoms.jsonl")
    
    with infectious_path.open('w', encoding='utf-8') as f:
        for item in infectious_data:
            f.write(json.dumps(item) + '\n')
    
    logger.info(f"✓ Infectious dataset: {len(infectious_data)} examples → {infectious_path}")
    
    # === DATASET 3: BALANCED (50/50 Mix) ===
    logger.info("\n=== Creating Balanced Dataset ===")
    
    half = dataset_size // 2
    balanced_atoms = results[:half] + results[-(half):]  # Top half + bottom half
    
    balanced_data = []
    for i, atom in enumerate(balanced_atoms):
        is_infectious = i < half
        example = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a knowledge system that balances memorability with accuracy."
                },
                {
                    "role": "user",
                    "content": f"What do you know about: {atom['predicate'].replace('_', ' ')}"
                },
                {
                    "role": "assistant",
                    "content": atom['object']
                }
            ],
            "metadata": {
                "dataset": "balanced",
                "is_infectious": is_infectious,
                "infectiousness_score": atom['infectiousness_score'],
                "confidence": atom['confidence'],
                "predicate": atom['predicate']
            }
        }
        balanced_data.append(example)
    
    balanced_path = Path("datasets/balanced_atoms.jsonl")
    
    with balanced_path.open('w', encoding='utf-8') as f:
        for item in balanced_data:
            f.write(json.dumps(item) + '\n')
    
    logger.info(f"✓ Balanced dataset: {len(balanced_data)} examples → {balanced_path}")
    
    # === STATISTICS ===
    logger.info("\n=== Dataset Statistics ===")
    
    control_avg = sum(a['confidence'] for a in control_atoms) / len(control_atoms)
    infectious_avg = sum(a['infectiousness_score'] for a in infectious_atoms) / len(infectious_atoms)
    
    stats = {
        "total_atoms_analyzed": total_atoms,
        "dataset_size": dataset_size,
        "datasets": {
            "control": {
                "path": str(control_path),
                "examples": len(control_data),
                "avg_confidence": round(control_avg, 3),
                "description": "Random sample - baseline"
            },
            "infectious": {
                "path": str(infectious_path),
                "examples": len(infectious_data),
                "avg_infectiousness": round(infectious_avg, 3),
                "description": "Top memetic fitness - self-replicating patterns"
            },
            "balanced": {
                "path": str(balanced_path),
                "examples": len(balanced_data),
                "description": "50/50 mix - control for dataset size"
            }
        },
        "next_steps": [
            "1. Upload datasets to fine-tuning platform (OpenAI, Anthropic, etc.)",
            "2. Fine-tune 3 separate models (one per dataset)",
            "3. Test each model on same prompts",
            "4. Compare: Does infectious model generate more self-replicating ideas?",
            "5. Measure: Jury acceptance rate, cross-domain connectivity, replication patterns"
        ]
    }
    
    # Save statistics
    stats_path = Path("datasets/dataset_stats.json")
    with stats_path.open('w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)
    
    logger.info(f"\n✓ Statistics saved → {stats_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("INFECTIOUS ATOM DATASETS READY")
    print("="*60)
    print(f"\nTotal atoms analyzed: {total_atoms}")
    print(f"Examples per dataset: {dataset_size}")
    print(f"\nDatasets created:")
    print(f"  1. Control:    {control_path}")
    print(f"  2. Infectious: {infectious_path}")
    print(f"  3. Balanced:   {balanced_path}")
    print(f"\nStatistics: {stats_path}")
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    for step in stats['next_steps']:
        print(f"  {step}")
    print("\n")
    
    await store.close()


if __name__ == "__main__":
    asyncio.run(prepare_datasets())
