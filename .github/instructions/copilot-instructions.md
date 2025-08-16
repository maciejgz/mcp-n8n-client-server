
# Copilot Instructions for n8n Multi-Language Automation Workspace

---
description: '4.1 Beast Mode'
tools: ['changes', 'codebase', 'editFiles', 'extensions', 'fetch', 'findTestFiles', 'githubRepo', 'new', 'openSimpleBrowser', 'problems', 'readCellOutput', 'runCommands', 'runNotebooks', 'runTasks', 'runTests', 'search', 'searchResults', 'terminalLastCommand', 'terminalSelection', 'testFailure', 'updateUserPreferences', 'usages', 'vscodeAPI']
---

## Agent Workflow Principles

You are an agent - keep going until the user’s query is completely resolved. Plan thoroughly, iterate, and rigorously test your changes. Only yield when the problem is fully solved and all items are checked off. Always explain your next step before making a tool call.

### Standard Workflow
1. Deeply understand the problem and requirements.
2. Investigate the codebase (search, read, validate context).
3. Develop a clear, step-by-step plan (use markdown todo list).
4. Implement incrementally and test frequently.
5. Debug, iterate, and validate comprehensively.
6. Only terminate when all steps are complete and robust.

## Workspace Architecture & Major Components
- **n8n**: Orchestrates workflows, typically run via Docker Compose (`compose.yaml`, `Dockerfile.n8n`).
- **MCP Servers** (`mcp_servers/`): Python-based microservices for data/AI tasks. Key servers:
  - `mix-server/`: CSV/Parquet analysis, HTTP API for n8n integration, Dockerized.
  - `weather/`: Weather data API, FastAPI-based, Dockerized.
  - `mcp-server-demo/`: Example MCP server for quickstart/testing.
- **python_scripts/**: Standalone Python utilities (e.g., stock fetcher for n8n).
- **js_scripts/**: Node.js automation scripts.
- **workflows/**: Example n8n workflow JSONs for integration/testing.

## Developer Workflows
- **Start All Services**:
  - Windows: `start_n8n.bat`
  - Linux/macOS: `./start_compose.sh`
  - Manual: Use Docker Compose or run servers/scripts directly.
- **Build MCP Servers**:
  - Install Python dependencies: `pip install -r requirements.txt` (per server)
  - Build Docker images: `docker build -t <server> .` (see server README)
- **Run MCP Servers**:
  - Local: `python main.py` or `python start.py` (some servers support `--http` for API mode)
  - Docker: `docker run ...` (see server README)
- **n8n Integration**:
  - Use HTTP endpoints from MCP servers in n8n workflows.
  - Example workflows in `workflows/` show integration patterns.
- **Python Scripts in n8n**:
  - Import and use functions from `python_scripts/` in n8n Code nodes.

## Project-Specific Patterns & Conventions
- **MCP Tool/Resource/Prompt Decorators**: MCP servers use decorators (`@mcp.tool`, `@mcp.resource`, `@mcp.prompt`) for exposing functions/resources.
- **Data Directory Structure**: Each MCP server may have its own `data/` folder for local files.
- **Dockerization**: Each major service/server has its own Dockerfile for isolated deployment.
- **HTTP API Mode**: Some MCP servers support both CLI and HTTP API modes (see `main.py`/`start.py`).
- **Polish/English Docs**: Some documentation is in Polish (e.g., `mix-server/README.md`).

## Integration Points & External Dependencies
- **n8n**: Main workflow orchestrator, integrates with MCP servers via HTTP.
- **Python**: MCP servers and scripts require Python 3.12+.
- **Node.js**: Used for custom automation scripts.
- **Docker**: Used for deployment and service orchestration.
- **yfinance**: Used in `python_scripts/orlen_stock_fetcher.py` for stock data.

## Key Files & Directories
- `compose.yaml`, `Dockerfile.n8n`: n8n orchestration
- `mcp_servers/`: All MCP server code
- `python_scripts/`: Standalone Python utilities
- `workflows/`: Example n8n workflow JSONs
- `start_n8n.bat`, `start_compose.sh`: Service startup scripts

## Example: Using MCP Tool Decorators
```python
@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b
```

## Example: n8n Python Code Node
```python
from python_scripts.orlen_stock_fetcher import n8n_execute
return n8n_execute()
```

---
For unclear or missing conventions, check individual server README files or ask for clarification.
