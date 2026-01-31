# Experiment Guide

## The Hypothesis

**Can universal principles from physics bootstrap AGI?**

This system tests whether implementing:
1. **Georgiev's Average Action Efficiency (AAE)** - True computational cost
2. **Gershenson's Complexity Balance** - Entropy vs Integration
3. **Bak's Self-Organized Criticality** - Edge of chaos operation

...can create conditions for intelligence to **self-organize** without explicit programming.

## Current Results

### Cycle 21: Entropy Unlock
- **Problem**: Added 56 papers → entropy stayed flat at 0.458
- **Cause**: Standard retrieval activated same conceptual neighborhoods
- **Solution**: MMR + entropy injection
- **Result**: Entropy jumped to 0.714 (+56%)

### Cycle 22: True Metrics
- **AAE**: 0.0023 (2.3 events per 1000 action units)
- **Entropy**: 0.506
- **Integration**: 0.683
- **Ratio I/H**: 0.74 (SUBCRITICAL - too ordered)
- **Status**: Need more chaos to reach critical point

## Running Your Own Experiment

### Basic Cycle

```python
# 1. Start measurement
start_action_cycle(cycle_id="C1")

# 2. Inject entropy (break conceptual neighborhoods)
inject_entropy_antipodal(
    user_id="alice",
    current_context="your current topic"
)

# 3. Retrieve with diversity
mmr_retrieve(
    user_id="alice",
    query="your query",
    lambda_param=0.6  # 0=relevance only, 1=diversity only
)

# 4. Record true cost
record_action(
    operation="experiment_step",
    tokens_used=X,
    latency_ms=Y,
    success=True
)

# 5. Check criticality
criticality_state()

# 6. Get efficiency
end_action_cycle()
```

### Measuring Entropy Unlock

**Hypothesis**: Diversity-aware retrieval increases entropy.

```python
# Baseline
entropy_stats(user_id="alice")  # Note initial entropy

# Intervention
inject_entropy_random(user_id="alice", n_domains=5)

# Measure
entropy_stats(user_id="alice")  # Compare to baseline
```

**Expected**: Entropy increases, normalized entropy approaches 1.0.

### Testing Criticality

**Hypothesis**: System performs best at critical point (I/H ≈ 1.0).

```python
# Check current zone
criticality_state()

# If SUBCRITICAL (I/H < 0.8):
#   - Inject more entropy
#   - Lower confidence on clustered atoms
#   - Ingest from diverse domains

# If SUPERCRITICAL (I/H > 1.2):
#   - Increase integration
#   - Strengthen connections
#   - Consolidate knowledge

# If CRITICAL (0.8 < I/H < 1.2):
#   - Maintain balance
#   - Look for emergence signatures
```

### Knowledge Ingestion with Provenance

**Hypothesis**: Real citations enable verification and trust.

```python
# Search for papers
search_arxiv(query="self-organized criticality")

# Ingest with provenance
ingest_arxiv(arxiv_id="1234.5678")

# Verify provenance
# Claims stored with:
# - ArXiv URL
# - Authors
# - Quoted spans
# - Content hash
```

### Self-Improvement Cycles

**Hypothesis**: System can generate valid hypotheses about itself.

```python
# Run improvement cycle
self_improve_cycle()

# Returns:
# - Hypotheses generated
# - Hypotheses applied
# - Success rate

# Track over time:
# - Do hypotheses improve?
# - Does AAE increase?
# - Does criticality approach 1.0?
```

## Metrics to Track

### Efficiency (AAE)
- **Formula**: events / total_action
- **Units**: events per action unit (token·ms)
- **Goal**: Increase over time (more events per unit cost)

### Entropy (H)
- **Formula**: -Σ(p·log₂(p)) for domain distribution
- **Range**: 0 (ordered) to 1 (chaotic)
- **Goal**: Balance with integration

### Integration (I)
- **Formula**: Mean confidence × (1 - entropy)
- **Range**: 0 (disconnected) to 1 (unified)
- **Goal**: Balance with entropy

### Criticality Ratio (I/H)
- **Formula**: Integration / Entropy
- **Zones**:
  - < 0.8: SUBCRITICAL (too ordered)
  - 0.8-1.2: CRITICAL (optimal)
  - > 1.2: SUPERCRITICAL (too chaotic)
- **Goal**: Maintain in critical zone

## Advanced Experiments

### K-Sweep (Workspace Capacity)
Test if there's a phase transition at specific workspace sizes.

```python
for k in [0, 2, 4, 6, 8]:
    # Activate K memories
    # Measure integration
    # Look for discontinuity (phase transition)
```

### Entropy Injection Strategies
Compare different methods:
- Antipodal (maximally distant)
- Random (diverse domains)
- Temporal (old + recent)

### MMR Lambda Sweep
Test relevance vs diversity tradeoff:

```python
for lambda_param in [0.0, 0.3, 0.6, 0.9]:
    mmr_retrieve(query="test", lambda_param=lambda_param)
    # Measure diversity of results
```

## Reproducibility

All experiments should:
1. **Start with clean state** or document initial conditions
2. **Record all parameters** (cycle_id, lambda, n_domains, etc.)
3. **Track metrics** (AAE, entropy, integration, ratio)
4. **Log provenance** (what papers, what operations)
5. **Share results** (GitHub issues, discussions)

## Contributing Experiments

If you discover:
- New entropy injection strategies
- Better criticality metrics
- Evidence of emergence
- Phase transitions

Please share:
1. Open an issue with results
2. Include reproduction steps
3. Attach metrics/logs
4. Propose hypothesis

## Open Questions

1. **Does criticality predict performance?** Measure task success at different I/H ratios.
2. **Can the system self-organize?** Track if AAE improves without intervention.
3. **Is there a phase transition?** Look for discontinuities in metrics.
4. **Do universal principles generalize?** Test on different domains.

## Citation

If you publish results:
```bibtex
@software{pltm2026,
  author = {Alby},
  title = {PLTM: Testing Universal Principles for AGI},
  year = {2026},
  url = {https://github.com/Alby2007/pltm-mcp}
}
```
