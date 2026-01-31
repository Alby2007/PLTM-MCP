# Quick Start Guide

## 5-Minute Setup

### 1. Install
```bash
git clone https://github.com/Alby2007/pltm-mcp.git
cd pltm-mcp
pip install -r requirements.txt
```

### 2. Configure Claude Desktop

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Linux**: `~/.config/Claude/claude_desktop_config.json`

Add:
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

Replace with your actual path. Use forward slashes.

### 3. Restart Claude Desktop

The server auto-starts.

### 4. Test

In Claude Desktop:
```
Use entropy_stats to check system state
```

Success! You should see entropy/integration metrics.

## First Experiment

Try this in Claude Desktop:

```
Let's run an experiment cycle:

1. start_action_cycle with cycle_id "test1"
2. inject_entropy_antipodal with context "machine learning"
3. criticality_state to see current zone
4. record_action for operation "test" with 100 tokens, 50ms latency, success true
5. end_action_cycle to get efficiency
```

You should see:
- Entropy injection results
- Criticality metrics (entropy, integration, ratio)
- Action recorded
- AAE (Average Action Efficiency) calculated

## What's Happening

The system is testing if **universal principles from physics** can bootstrap AGI:

1. **Georgiev AAE** - True computational efficiency (events/action)
2. **Gershenson Complexity** - Balance entropy (H) vs integration (I)
3. **Bak Criticality** - Self-organized criticality at edge of chaos

**Goal**: Push system to critical point (I/H ratio → 1.0) where emergence happens.

## Next Steps

- Read [README.md](./README.md) for full tool list
- Try different entropy injection strategies
- Ingest ArXiv papers with provenance
- Monitor criticality state over time

## Troubleshooting

**Server not connecting?**
```bash
# Check logs
cat "%APPDATA%\Claude\logs\mcp-server-pltm-memory.log"

# Test manually
python server.py
```

**Import errors?**
```bash
pip install --upgrade -r requirements.txt
```

**Tools timing out?**
- Restart Claude Desktop after any code changes
- Check database isn't too large (>10k atoms)

## Support

- Issues: [github.com/Alby2007/pltm-mcp/issues](https://github.com/Alby2007/pltm-mcp/issues)
- Discussions: [github.com/Alby2007/pltm-mcp/discussions](https://github.com/Alby2007/pltm-mcp/discussions)
