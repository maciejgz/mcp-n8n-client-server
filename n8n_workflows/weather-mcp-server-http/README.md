# weather-mcp-server-http Workflow Documentation

This workflow integrates OpenAI chat, an AI agent, and a weather MCP server using n8n.

## Project Components Usage
This workflow uses components and services provided by the project, especially the weather-mcp-server and AI tools defined in the repository. Make sure all required services are running according to the instructions in the main project README.

## Workflow Overview
- **AI Agent:** Handles orchestration and decision-making.
- **OpenAI Chat Model:** Uses GPT-4.1-mini for language understanding.
- **weather-mcp-server:** Connects to a weather MCP server via HTTP to fetch weather data.

## Node Descriptions
- **When chat message received:** Triggers the workflow on incoming chat messages.
- **OpenAI Chat Model:** Provides LLM capabilities using OpenAI API.
- **AI Agent:** Orchestrates AI actions and tool usage.
- **weather-mcp-server:** Connects to weather MCP server for weather info.

## Configuration
The workflow configuration is stored in `../weather-mcp-server-http.json`.

- Make sure the weather MCP server is running and accessible at `http://weather-mcp-server:8000/mcp`.
- OpenAI API credentials must be set up in n8n.

---
For more details, see the workflow JSON file or contact the project maintainer.
