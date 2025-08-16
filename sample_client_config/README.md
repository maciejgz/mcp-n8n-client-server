Here is an example of the client configuration file for http and stdio MCP server connection:
```
{
  "globalShortcut": "",
  "mcpServers": {
    "Demo": {
      "command": "C:\\Users\\maciej\\.local\\bin\\uv.EXE",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "C:\\workspaces\\n8n\\mcp_servers\\mcp-server-demo\\server.py"
      ]
    },
    "Weather": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8000/mcp"
      ]
    }
  }
}
```