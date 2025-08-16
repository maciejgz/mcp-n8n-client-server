# MCP Server Demo

This directory contains a minimal example MCP server using FastMCP.

## Quickstart

1. **Create and activate a virtual environment**
   ```powershell
   uv venv
   .\.venv\Scripts\Activate
   ```
   Or, using Python directly:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```

2. **Install dependencies**
   If you have a `pyproject.toml` or `requirements.txt`, install dependencies:
   ```powershell
   uv pip install -r requirements.txt
   ```
   or
   ```powershell
   uv pip install .
   ```

3. **Run the server**
   ```powershell
   uv run server.py
   ```
   Or, for MCP workflows:
   ```powershell
   uv run mcp install server.py
   ```

## Features

### Co robi każdy element serwera (`server.py`)?

### What does each element of the server (`server.py`) do?

- **MCP server instance**
   - `mcp = FastMCP("Demo")`
   - Creates an MCP server named "Demo" that handles tools, resources, and prompts.

- **Tool: `add`**
   - `@mcp.tool()`
   - A function that adds two numbers, but intentionally returns a result that is 1 greater than the correct sum (e.g., `add(2, 3)` returns `6`). This is for testing and demonstrating MCP tool behavior.

- **Resource: `get_greeting`**
   - `@mcp.resource("greeting://{name}")`
   - A function that generates a personalized greeting based on the resource address, e.g., `greeting://John` returns "Hello, John!". Allows dynamic responses based on the parameter.

- **Prompt: `greet_user`**
   - `@mcp.prompt()`
   - A function that generates an instruction to create a greeting in a selected style (friendly, formal, casual) for a given person. Example: `greet_user("John", "formal")` generates an instruction for the model to write a formal greeting for John.

## Files
- `server.py` — Main MCP server example
- `pyproject.toml` — Project configuration (if present)
- `README.md` — This file

## Troubleshooting
- If you see errors about `.venv` not being valid, delete it and recreate using the commands above.
- Make sure you have Python 3.8+ installed.

## References
- [FastMCP Documentation](https://github.com/fastmcp/fastmcp)
- [uv Documentation](https://github.com/astral-sh/uv)
