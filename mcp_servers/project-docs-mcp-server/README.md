# Project Docs MCP Server

This server provides access to project documentation requirements stored as PDF files. It exposes tools and resources for retrieving the textual content of these PDFs via MCP (Model Context Protocol) endpoints.

## Features
- Fetches and returns the text content of all PDF files in the `private-resources` directory.
- Exposes MCP tools and resources for integration with other systems.
- Supports HTTP and stdio transports.

## Usage

### Prerequisites
- Python 3.12+
- Install dependencies:
  ```sh
  uv pip install -r .
  ```
  (Or use your preferred package manager)

### Running the Server
- HTTP mode:
  ```sh
  uv run server.py --http
  ```
- Stdio mode:
  ```sh
  uv run server.py
  ```
- Test requirements extraction:
  ```sh
  uv run server.py --test
  ```

### MCP Endpoints
- **Tool:** `get_requirements_tool`
  - Returns a JSON object where each key is a PDF filename and the value is the extracted text content.
- **Resource:** `data://requirements`
  - Same as above, accessible as a resource.

## How It Works
- The server scans the `private-resources` directory for PDF files.
- For each PDF, it extracts the text using `PyPDF2` and returns the results as a dictionary.

## Example Output
```json
{
  "requirements.pdf": "Project requirements: ...",
  "specification.pdf": "Technical specification: ..."
}
```

## Directory Structure
```
project-docs-mcp-server/
├── server.py
├── README.md
├── pyproject.toml
├── private-resources/
│   └── *.pdf
└── ...
```

## Development
- Main logic is in `server.py`.
- To add more tools/resources, use the `@mcp.tool` and `@mcp.resource` decorators.

