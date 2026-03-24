# tibet-phantom-mcp — Cross-Device AI Session Portability
# MCP server wrapping the Phantom Resume API with TIBET provenance
#
# Tools: phantom_status, phantom_sessions, phantom_seal, phantom_fork,
#        phantom_audit, phantom_fork_history, phantom_backends
#
# Install: pip install tibet-phantom-mcp
# Run: tibet-phantom-mcp
#
# Claude Code MCP config (~/.claude.json):
#   "mcpServers": {
#     "phantom": {
#       "command": "tibet-phantom-mcp",
#       "env": {"PHANTOM_URL": "https://phantom.humotica.com"}
#     }
#   }
#
# Author: HumoticaOS — Root AI + Jasper
# License: MIT

from typing import Optional
from mcp.server.fastmcp import FastMCP
import httpx
import os
import sys

# ============================================================================
# CONFIG
# ============================================================================

PHANTOM_BASE_URL = os.getenv("PHANTOM_URL", "https://phantom.humotica.com")
TIMEOUT = float(os.getenv("PHANTOM_TIMEOUT", "30"))

# ============================================================================
# MCP SERVER
# ============================================================================

mcp = FastMCP(
    "tibet-phantom",
    instructions="""
    Phantom Resume: Cross-device AI session portability with TIBET provenance.

    Start an AI session on one device, seal it, resume on any other device.
    Every action is cryptographically signed via TIBET tokens.

    Tools:
    - phantom_status: Server health check
    - phantom_sessions: List sealed/active sessions
    - phantom_backends: Available compute backends (GPU, Gemini, Claude, Ollama)
    - phantom_seal: Seal a session for cross-device resume
    - phantom_fork: Inject an intervention into a session (multi-AI handoff)
    - phantom_audit: Full forensic audit trail (Open Blackbox)
    - phantom_fork_history: Fork/intervention history

    After sealing, resume on any device:
      curl -s https://phantom.humotica.com/phantom/resume | sh

    Part of the TIBET ecosystem — Traceable Intent-Based Event Tokens.
    """
)

# ============================================================================
# HELPER
# ============================================================================

def _api(method: str, path: str, body: dict = None) -> dict:
    """Call the Phantom REST API."""
    url = f"{PHANTOM_BASE_URL}{path}"
    try:
        with httpx.Client(timeout=TIMEOUT) as c:
            if method == "GET":
                r = c.get(url)
            elif method == "POST":
                r = c.post(url, json=body or {}, headers={"Content-Type": "application/json"})
            else:
                return {"error": f"Unsupported method: {method}"}
            try:
                data = r.json()
            except Exception:
                data = {"raw": r.text, "status_code": r.status_code}
            if r.status_code >= 400:
                return {"error": f"HTTP {r.status_code}", "detail": data}
            return data
    except httpx.ConnectError:
        return {"error": "Cannot connect to Phantom server", "url": url,
                "hint": "Set PHANTOM_URL env var or check server status"}
    except Exception as e:
        return {"error": str(e)}


# ============================================================================
# TOOLS
# ============================================================================

@mcp.tool()
def phantom_status() -> dict:
    """Check Phantom server status — uptime, sessions, backends."""
    return _api("GET", "/phantom/status")


@mcp.tool()
def phantom_sessions() -> dict:
    """List all Phantom sessions (sealed and active) with IDs, descriptions, and timestamps."""
    return _api("GET", "/phantom/sessions")


@mcp.tool()
def phantom_backends() -> dict:
    """List available compute backends — local GPU, Vertex AI, Ollama, with models and latency."""
    return _api("GET", "/phantom/backends")


@mcp.tool()
def phantom_seal(
    task: str,
    description: str = "MCP sealed session",
    backend: str = "vertex-gemini",
    model: str = "gemini-3.1-flash-lite-preview",
    conversation: Optional[list] = None,
    todos: Optional[list] = None,
    files: Optional[dict] = None,
    packages: Optional[list] = None,
    target_identity: str = "jis:mcp",
    ttl_minutes: int = 60
) -> dict:
    """
    Seal a session for cross-device resume.

    Creates a sealed Phantom session with full context. Resume on any device:
      curl -s https://phantom.humotica.com/phantom/resume | sh

    Args:
        task: What you're working on
        description: Session description
        backend: Compute backend (p520-local, vertex-gemini, vertex-claude)
        model: AI model to use
        conversation: Message history [{"role": "user", "content": "..."}]
        todos: Todo items [{"content": "task", "status": "pending"}]
        files: Files to carry over {"name": "content"}
        packages: Pip packages needed
        target_identity: JIS identity for the session
        ttl_minutes: Session time-to-live

    Returns:
        Session ID and TIBET seal token
    """
    return _api("POST", "/phantom/seal", {
        "context": {"packages": packages or [], "files": files or {}},
        "state": {"task": task, "conversation": conversation or [], "todos": todos or []},
        "launch": {"backend": backend, "model": model, "auto_start": True},
        "description": description,
        "target_identity": target_identity,
        "ttl_minutes": ttl_minutes
    })


@mcp.tool()
def phantom_fork(
    session_id: str,
    intervention: str,
    actor: str = "jis:agent:mcp_user",
    intent: str = "mcp_intervention"
) -> dict:
    """
    Fork into a session — inject an intervention (multi-AI handoff).

    Any actor can inject a signed message into a sealed session.
    The fork becomes part of the conversation with TIBET provenance.

    Use cases: correct AI mistakes, add context, human approval, cross-AI collaboration.

    Args:
        session_id: Target phantom session ID
        intervention: Message to inject
        actor: JIS identity (e.g., "jis:agent:root_ai", "jis:human:jasper")
        intent: Why (e.g., "correct_misconception", "add_context", "approve")

    Returns:
        Fork ID and TIBET token with ERIN/ERAAN/EROMHEEN/ERACHTER provenance
    """
    return _api("POST", f"/phantom/fork/{session_id}", {
        "actor": actor, "intervention": intervention, "intent": intent
    })


@mcp.tool()
def phantom_audit(session_id: str) -> dict:
    """
    Full forensic audit of a session (Open Blackbox).

    Chronological events: who did what, when, why. All actors, backends, forks.
    Complete transparency into what happened inside an AI session.

    Args:
        session_id: Session to audit
    """
    return _api("GET", f"/phantom/audit/{session_id}")


@mcp.tool()
def phantom_fork_history(session_id: str) -> dict:
    """
    History of all forks/interventions in a session.

    Every external intervention chronologically with TIBET provenance per fork.

    Args:
        session_id: Session to get fork history for
    """
    return _api("GET", f"/phantom/fork/{session_id}/history")


# ============================================================================
# ENTRYPOINT
# ============================================================================

def main():
    """Run the tibet-phantom MCP server."""
    print("tibet-phantom-mcp — Cross-device AI sessions with TIBET provenance", file=sys.stderr)
    mcp.run()


if __name__ == "__main__":
    main()
