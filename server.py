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
        Tool(
            name="tldr_extract",
            description="Extract full file analysis (classes, functions, methods, imports). Use to deeply understand a single file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "File path to analyze"},
                    "class_filter": {"type": "string", "description": "Filter to specific class"},
                    "function_filter": {"type": "string", "description": "Filter to specific function"},
                    "method_filter": {"type": "string", "description": "Filter to specific method (Class.method)"},
                },
                "required": ["file"],
            },
        ),
        Tool(
            name="tldr_cfg",
            description="Control flow graph for a function. Shows branches, loops, and execution paths.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "Source file path"},
                    "function": {"type": "string", "description": "Function name"},
                    "lang": {"type": "string", "description": "Language override (auto-detected if omitted)"},
                },
                "required": ["file", "function"],
            },
        ),
        Tool(
            name="tldr_dfg",
            description="Data flow graph for a function. Shows how data moves through variables and expressions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "Source file path"},
                    "function": {"type": "string", "description": "Function name"},
                    "lang": {"type": "string", "description": "Language override (auto-detected if omitted)"},
                },
                "required": ["file", "function"],
            },
        ),
        Tool(
            name="tldr_slice",
            description="Program slice: find all lines that affect a specific line. Use to understand what influences a value or statement.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "Source file path"},
                    "function": {"type": "string", "description": "Function name"},
                    "line": {"type": "integer", "description": "Line number to slice from"},
                    "direction": {"type": "string", "enum": ["backward", "forward"], "description": "Slice direction (default: backward)"},
                    "var": {"type": "string", "description": "Variable to track (optional)"},
                },
                "required": ["file", "function", "line"],
            },
        ),
        Tool(
            name="tldr_dead",
            description="Find unreachable (dead) code in a project. Useful for cleanup and refactoring.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Project path (absolute)"},
                    "lang": {"type": "string", "description": "Language filter"},
                    "entry": {"type": "array", "items": {"type": "string"}, "description": "Additional entry point patterns"},
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="tldr_imports",
            description="Parse imports from a source file. Shows all dependencies of a file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "Source file path"},
                    "lang": {"type": "string", "description": "Language override"},
                },
                "required": ["file"],
            },
        ),
        Tool(
            name="tldr_importers",
            description="Find all files that import a module (reverse import lookup). Use to understand module usage across the project.",
            inputSchema={
                "type": "object",
                "properties": {
                    "module": {"type": "string", "description": "Module name to search for"},
                    "path": {"type": "string", "description": "Project path (absolute)"},
                    "lang": {"type": "string", "description": "Language filter"},
                },
                "required": ["module", "path"],
            },
        ),
        Tool(
            name="tldr_change_impact",
            description="Find tests affected by changed files. Use before committing to know what to test.",
            inputSchema={
                "type": "object",
                "properties": {
                    "files": {"type": "array", "items": {"type": "string"}, "description": "Files to analyze"},
                    "git": {"type": "boolean", "description": "Use git diff to find changed files"},
                    "git_base": {"type": "string", "description": "Git ref to diff against (default: HEAD~1)"},
                    "lang": {"type": "string", "description": "Language filter"},
                    "depth": {"type": "integer", "description": "Max call graph depth (default: 5)"},
                },
                "required": [],
            },
        ),
        Tool(
            name="tldr_diagnostics",
            description="Get type-check and lint diagnostics for a file or project. Use to find errors without running the code.",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "File or project directory to check"},
                    "project": {"type": "boolean", "description": "Check entire project instead of single file"},
                    "no_lint": {"type": "boolean", "description": "Skip linter, only run type checker"},
                    "lang": {"type": "string", "description": "Language override"},
                },
                "required": ["target"],
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

    elif name == "tldr_extract":
        args = ["extract", arguments["file"]]
        if "class_filter" in arguments:
            args += ["--class", arguments["class_filter"]]
        if "function_filter" in arguments:
            args += ["--function", arguments["function_filter"]]
        if "method_filter" in arguments:
            args += ["--method", arguments["method_filter"]]
        output = run_tldr(args)

    elif name == "tldr_cfg":
        args = ["cfg", arguments["file"], arguments["function"]]
        if "lang" in arguments:
            args += ["--lang", arguments["lang"]]
        output = run_tldr(args)

    elif name == "tldr_dfg":
        args = ["dfg", arguments["file"], arguments["function"]]
        if "lang" in arguments:
            args += ["--lang", arguments["lang"]]
        output = run_tldr(args)

    elif name == "tldr_slice":
        args = ["slice", arguments["file"], arguments["function"], str(arguments["line"])]
        if "direction" in arguments:
            args += ["--direction", arguments["direction"]]
        if "var" in arguments:
            args += ["--var", arguments["var"]]
        output = run_tldr(args)

    elif name == "tldr_dead":
        args = ["dead", arguments["path"]]
        if "lang" in arguments:
            args += ["--lang", arguments["lang"]]
        if "entry" in arguments:
            for e in arguments["entry"]:
                args += ["--entry", e]
        output = run_tldr(args)

    elif name == "tldr_imports":
        args = ["imports", arguments["file"]]
        if "lang" in arguments:
            args += ["--lang", arguments["lang"]]
        output = run_tldr(args)

    elif name == "tldr_importers":
        args = ["importers", arguments["module"], arguments["path"]]
        if "lang" in arguments:
            args += ["--lang", arguments["lang"]]
        output = run_tldr(args)

    elif name == "tldr_change_impact":
        args = ["change-impact"]
        if "git" in arguments and arguments["git"]:
            args += ["--git"]
        if "git_base" in arguments:
            args += ["--git-base", arguments["git_base"]]
        if "lang" in arguments:
            args += ["--lang", arguments["lang"]]
        if "depth" in arguments:
            args += ["--depth", str(arguments["depth"])]
        if "files" in arguments:
            args += arguments["files"]
        output = run_tldr(args)

    elif name == "tldr_diagnostics":
        args = ["diagnostics", arguments["target"]]
        if "project" in arguments and arguments["project"]:
            args += ["--project"]
        if "no_lint" in arguments and arguments["no_lint"]:
            args += ["--no-lint"]
        if "lang" in arguments:
            args += ["--lang", arguments["lang"]]
        output = run_tldr(args)

    else:
        output = f"Unknown tool: {name}"

    return [TextContent(type="text", text=output)]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())