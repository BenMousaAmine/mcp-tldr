
# mcp-tldr

MCP server that exposes https://github.com/parcadei/llm-tldr code analysis tools to Claude Code (or any MCP client).

## Prerequisites

- Python 3.11+
- `tldr` CLI installed and in your PATH ([install instructions](https://github.com/parcadei/llm-tldr))

## Setup

```bash
git clone https://github.com/YOUR_USER/mcp-tldr.git
cd mcp-tldr
python3 -m venv .venv
.venv/bin/pip install -e .
```

## Add to Claude Code

Add this to your `~/.claude.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "tldr": {
      "type": "stdio",
      "command": "/absolute/path/to/mcp-tldr/.venv/bin/python",
      "args": ["server.py"],
      "cwd": "/absolute/path/to/mcp-tldr"
    }
  }
}
```

Replace `/absolute/path/to/mcp-tldr` with the actual path where you cloned the repo.

Alternatively, if `tldr` is not in your PATH, set the `TLDR_BIN` environment variable:

```json
{
  "tldr": {
    "type": "stdio",
    "command": "/absolute/path/to/mcp-tldr/.venv/bin/python",
    "args": ["server.py"],
    "cwd": "/absolute/path/to/mcp-tldr",
    "env": {
      "TLDR_BIN": "/path/to/tldr"
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `tldr_tree` | File tree of a project |
| `tldr_structure` | Code structure (classes, functions, imports) |
| `tldr_context` | LLM-ready context for a function/class |
| `tldr_search` | Pattern search across files |
| `tldr_impact` | Find all callers of a function |
| `tldr_calls` | Cross-file call graph |
| `tldr_semantic` | Natural language code search |
| `tldr_arch` | Detect architectural layers |
| `tldr_warm` | Pre-build cache for faster queries |
| `tldr_extract` | Full file analysis (classes, functions, methods) |
| `tldr_cfg` | Control flow graph for a function |
| `tldr_dfg` | Data flow graph for a function |
| `tldr_slice` | Program slice (what affects line X) |
| `tldr_dead` | Find unreachable/dead code |
| `tldr_imports` | Parse imports from a file |
| `tldr_importers` | Find all files importing a module |
| `tldr_change_impact` | Find tests affected by changes |
| `tldr_diagnostics` | Type-check and lint diagnostics |

## Usage

After setup, restart Claude Code. The tools will be available automatically. Example prompts:

- "Use tldr_tree to show the structure of this project"
- "Use tldr_context to explain the `handleAuth` function"
- "Use tldr_impact to see what calls `processPayment`"
