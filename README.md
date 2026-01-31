# PLTM MCP Server

**Procedural Long-Term Memory** - An MCP server for Claude Desktop that provides 78 tools for AGI experiments based on universal principles from physics.

## What This Does

Gives Claude Desktop access to:
- **Memory operations** - Store/retrieve facts as semantic triples
- **Diversity retrieval** - MMR, entropy injection, attention mechanisms
- **Meta-cognition** - Self-improvement, criticality monitoring
- **Knowledge ingestion** - ArXiv papers with real provenance
- **True metrics** - Action accounting, efficiency tracking

## Quick Start

### Prerequisites
- Claude Desktop
- Python 3.11+

### Installation

```bash
# Clone
git clone https://github.com/Alby2007/pltm-mcp.git
cd pltm-mcp

# Install
pip install -r requirements.txt

# Configure Claude Desktop
# Edit: %APPDATA%\Claude\claude_desktop_config.json (Windows)
#   or: ~/Library/Application Support/Claude/claude_desktop_config.json (Mac)
```

Add this to your config:
```json
{
  "mcpServers": {
    "pltm-memory": {
      "command": "python",
      "args": ["C:/absolute/path/to/pltm-mcp/server.py"]
    }
  }
}
```

Restart Claude Desktop. Done!

### Verify

In Claude Desktop:
```
Use entropy_stats to check system state
```

If you see metrics, it's working!

## Example Usage

```python
# Start experiment cycle
start_action_cycle(cycle_id="C1")

# Inject entropy to break conceptual neighborhoods
inject_entropy_antipodal(
    user_id="alice",
    current_context="machine learning"
)

# Retrieve with diversity
mmr_retrieve(
    user_id="alice",
    query="neural networks",
    lambda_param=0.6
)

# Track true computational cost
record_action(
    operation="mmr_diversity",
    tokens_used=450,
    latency_ms=180,
    success=True
)

# Check criticality state
criticality_state()

# End cycle
end_action_cycle()  # Returns AAE efficiency
```

## The Experiment

**Hypothesis**: Universal principles from physics (criticality, self-organization, emergence) can bootstrap AGI.

**Current Results**:
- Unlocked entropy bottleneck (+56% in Cycle 21)
- Measuring true computational efficiency (AAE = 0.0023)
- Testing if system can self-organize toward criticality

**Goal**: Push system to critical point where phase transitions occur and higher-order intelligence emerges.

## Tools (78 total)

### Memory
- `store_memory_atom`, `retrieve_memories`, `update_memory`, `delete_memory`

### Diversity Retrieval
- `mmr_retrieve` - Maximal Marginal Relevance
- `attention_retrieve`, `attention_multihead`

### Entropy Management
- `inject_entropy_antipodal` - Activate distant concepts
- `inject_entropy_random` - Sample diverse domains
- `inject_entropy_temporal` - Mix old + recent
- `entropy_stats` - Diagnose diversity

### Meta-Cognition
- `self_improve_cycle` - Generate/apply hypotheses
- `criticality_state` - Check edge of chaos
- `criticality_recommend` - Get adjustments

### Action Accounting
- `record_action`, `get_aae`, `start_action_cycle`, `end_action_cycle`

### Knowledge Ingestion
- `ingest_arxiv`, `search_arxiv`, `arxiv_history`

[Full tool list in server.py]

## Architecture

```
Memory Atoms (Triples)
  ↓
[subject] [predicate] [object]
  ↓
SQLite Graph Store
  ↓
Retrieval Systems (Standard/MMR/Attention)
  ↓
Meta-Cognitive Layer (Self-improvement/Criticality)
  ↓
MCP Tools (78 total)
```

## Troubleshooting

**Server not connecting?**
- Check logs: `%APPDATA%\Claude\logs\mcp-server-pltm-memory.log`
- Test manually: `python server.py`

**Tools timing out?**
- Restart Claude Desktop after code changes

**Import errors?**
```bash
pip install --upgrade -r requirements.txt
```

## Contributing

This is active research. Contributions welcome:
- New entropy strategies
- Better criticality metrics
- Additional universal principles
- Experiment protocols

## License

MIT

## Citation

```bibtex
@software{pltm2026,
  author = {Alby},
  title = {PLTM: Procedural Long-Term Memory MCP Server},
  year = {2026},
  url = {https://github.com/Alby2007/pltm-mcp}
}
```

## Links

- Issues: [github.com/Alby2007/pltm-mcp/issues](https://github.com/Alby2007/pltm-mcp/issues)
- Main Project: [github.com/Alby2007/LLTM](https://github.com/Alby2007/LLTM)
