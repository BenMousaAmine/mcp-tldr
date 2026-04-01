#!/usr/bin/env python3
"""MCP server wrapper for tldr code analysis tool."""

import os
import subprocess
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

TLDR_BIN = os.environ.get("TLDR_BIN", "tldr")

app = Server("tldr-mcp")


def run_tldr(args: list[str], cwd: str | None = None) -> str:
    """Run tldr command and return output."""
    cmd = [TLDR_BIN] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30,
        )
        output = result.stdout
        if result.returncode != 0 and result.stderr:
            output += f"\nSTDERR: {result.stderr}"
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: command timed out after 30s"
    except Exception as e:
        return f"Error: {e}"


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="tldr_tree",
            description="Show file tree of a project directory. Use instead of ls/find.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Project path (absolute)"},
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="tldr_structure",
            description="Show code structure (classes, functions, imports) for a project. Use instead of reading files to understand structure.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Project path (absolute)"},
                    "lang": {"type": "string", "description": "Language filter (python, typescript, php, swift, kotlin, etc.)"},
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="tldr_context",
            description="Get LLM-ready context for a function/class. Use INSTEAD of reading large files. Returns only relevant code.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Function or class name to get context for"},
                    "project": {"type": "string", "description": "Project path (absolute)"},
                },
                "required": ["symbol", "project"],
            },
        ),
        Tool(
            name="tldr_search",
            description="Search files for a pattern. Faster than grep for structural searches.",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Search pattern"},
                    "path": {"type": "string", "description": "Project path (absolute)"},
                },
                "required": ["pattern", "path"],
            },
        ),
        Tool(
            name="tldr_impact",
            description="Find all callers of a function (reverse call graph). Use to understand what breaks if you change a function.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Function name to find callers of"},
                    "path": {"type": "string", "description": "Project path (absolute)"},
                },
                "required": ["symbol", "path"],
            },
        ),
        Tool(
            name="tldr_calls",
            description="Build cross-file call graph starting from a function.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Function name"},
                    "path": {"type": "string", "description": "Project path (absolute)"},
                },
                "required": ["symbol", "path"],
            },
        ),
        Tool(
            name="tldr_semantic",
            description="Semantic code search using natural language. Use for conceptual searches like 'authentication logic' or 'payment handling'.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Natural language search query"},
                    "path": {"type": "string", "description": "Project path (absolute)"},
                },
                "required": ["query", "path"],
            },
        ),
        Tool(
            name="tldr_arch",
            description="Detect architectural layers from call patterns. Shows high-level architecture of the project.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Project path (absolute)"},
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="tldr_warm",
            description="Pre-build call graph cache for faster queries. Run once per project before using other tldr tools.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Project path (absolute)"},
                },
                "required": ["path"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "tldr_tree":
        output = run_tldr(["tree", arguments["path"]])

    elif name == "tldr_structure":
        args = ["structure", arguments["path"]]
        if "lang" in arguments:
            args += ["--lang", arguments["lang"]]
        output = run_tldr(args)

    elif name == "tldr_context":
        output = run_tldr([
            "context", arguments["symbol"],
            "--project", arguments["project"]
        ])

    elif name == "tldr_search":
        output = run_tldr(["search", arguments["pattern"], arguments["path"]])

    elif name == "tldr_impact":
        output = run_tldr(["impact", arguments["symbol"], arguments["path"]])

    elif name == "tldr_calls":
        output = run_tldr(["calls", arguments["symbol"], arguments["path"]])

    elif name == "tldr_semantic":
        output = run_tldr(["semantic", arguments["query"], arguments["path"]])

    elif name == "tldr_arch":
        output = run_tldr(["arch", arguments["path"]])

    elif name == "tldr_warm":
        output = run_tldr(["warm", arguments["path"]])

    else:
        output = f"Unknown tool: {name}"

    return [TextContent(type="text", text=output)]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())