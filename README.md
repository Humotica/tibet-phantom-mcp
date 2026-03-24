# tibet-phantom-mcp

**MCP server for Phantom Resume — cross-device AI session portability with TIBET provenance.**

Start an AI session on your laptop, seal it, walk to any other device, resume exactly where you left off. Every action is cryptographically signed via [TIBET](https://datatracker.ietf.org/doc/draft-vandemeent-tibet/) tokens.

Part of the [TIBET ecosystem](https://humotica.com) by [HumoticaOS](https://github.com/Humotica).

## Install

```bash
pip install tibet-phantom-mcp
```

## Claude Code / Claude Desktop Config

Add to your MCP settings:

```json
{
  "mcpServers": {
    "phantom": {
      "command": "tibet-phantom-mcp",
      "env": {
        "PHANTOM_URL": "https://phantom.humotica.com"
      }
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `phantom_status` | Server health check — uptime, sessions, backends |
| `phantom_sessions` | List all sealed/active sessions |
| `phantom_backends` | Available compute backends (GPU, Gemini, Claude, Ollama) |
| `phantom_seal` | Seal a session for cross-device resume |
| `phantom_fork` | Inject an intervention into a session (multi-AI handoff) |
| `phantom_audit` | Full forensic audit trail (Open Blackbox) |
| `phantom_fork_history` | History of all forks/interventions |

## How It Works

```
Device A                    Phantom Server              Device B
────────                    ──────────────              ────────
Start session ──────────►   Stores context
Work with AI                TIBET tokens
/exit ──────────────────►   Session sealed
                                                        curl .../resume | sh
                            ◄───────────────────────── Resume request
                            L4 integrity verify ──────► Session restored
                            TIBET chain intact           AI picks up where
                                                         you left off
```

### Multi-AI Fork

Any actor (human or AI) can fork into a session:

```python
# Claude corrects something Gemini said
phantom_fork(
    session_id="phantom-1234-abc",
    intervention="That's not quite right — TIBET uses hash chains, not blockchain.",
    actor="jis:agent:root_ai",
    intent="correct_misconception"
)
```

### Open Blackbox (Audit)

```python
# See exactly what happened inside a session
phantom_audit(session_id="phantom-1234-abc")
# → chronological events, all actors, backends, forks, TIBET provenance
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PHANTOM_URL` | `https://phantom.humotica.com` | Phantom server URL |
| `PHANTOM_TIMEOUT` | `30` | HTTP timeout in seconds |

## Related TIBET Packages

- [`tibet-audit`](https://pypi.org/project/tibet-audit/) — Core TIBET provenance
- [`tibet-triage`](https://pypi.org/project/tibet-triage/) — Process triage with HITL
- [`tibet-ipoll-mcp`](https://pypi.org/project/tibet-ipoll-mcp/) — AI-to-AI messaging MCP server
- [`tibet-pol`](https://pypi.org/project/tibet-pol/) — Machine health monitoring

## License

MIT — HumoticaOS
