# N8N MCP Client Configuration Guide

## Problem Diagnosis
The error "Could not connect to your MCP server" in n8n typically occurs due to configuration issues with the MCP Client node.

## Available Endpoints

Our MCP server provides multiple endpoints for different use cases:

### HTTP Endpoints
- **Health Check**: `http://localhost:8000/health`
- **MCP Protocol**: `http://localhost:8000/mcp` (GET/POST)
- **Tools List**: `http://localhost:8000/tools`
- **Direct Tool Call**: `http://localhost:8000/call-tool`
- **Test Connection**: `http://localhost:8000/test-connection`
- **N8N Integration**: `http://localhost:8000/n8n`
- **Server-Sent Events**: `http://localhost:8000/sse`

### WebSocket Endpoint
- **MCP Protocol**: `ws://localhost:8000/ws`

## N8N MCP Client Configuration Options

### Option 1: HTTP REST API (Recommended)
```
Server URL: http://mcp-server:8000/mcp
Protocol: HTTP
Method: GET for initialization, POST for tool calls
```

### Option 2: WebSocket Protocol
```
Server URL: ws://mcp-server:8000/ws
Protocol: WebSocket
Format: JSON-RPC 2.0
```

### Option 3: Docker Internal Network
If n8n and mcp-server are in the same Docker network:
```
Server URL: http://mcp-server:8000/mcp
```

### Option 4: Localhost (for testing)
If accessing from host machine:
```
Server URL: http://localhost:8000/mcp
```

## Testing Connection

Before configuring n8n, test the connection:

### Test 1: Basic Health Check
```bash
curl http://localhost:8000/health
```

### Test 2: MCP Protocol Test
```bash
curl http://localhost:8000/mcp
```

### Test 3: Connection Test
```bash
curl http://localhost:8000/test-connection
```

### Test 4: Tools List
```bash
curl http://localhost:8000/tools
```

## Common Issues & Solutions

### Issue 1: Connection Refused
- **Cause**: Server not running or wrong URL
- **Solution**: Check if container is running: `docker-compose ps`

### Issue 2: Network Issues
- **Cause**: N8N can't reach the MCP server
- **Solution**: Ensure both containers are in the same network

### Issue 3: Protocol Mismatch
- **Cause**: N8N expects different protocol format
- **Solution**: Try different endpoints (HTTP vs WebSocket)

### Issue 4: CORS Issues
- **Cause**: Browser blocking cross-origin requests
- **Solution**: Our server has CORS enabled for all origins

## Docker Network Configuration

Both services are configured in `compose.yaml`:
```yaml
services:
  n8n:
    depends_on:
      - mcp-server
    # n8n can reach mcp-server via http://mcp-server:8000

  mcp-server:
    ports:
      - "127.0.0.1:8000:8000"
    # Accessible from host via http://localhost:8000
```

## Debugging Steps

1. **Check container status**:
   ```bash
   docker-compose ps
   docker-compose logs mcp-server
   docker-compose logs n8n
   ```

2. **Test from inside n8n container**:
   ```bash
   docker-compose exec n8n curl http://mcp-server:8000/health
   ```

3. **Test from host**:
   ```bash
   curl http://localhost:8000/health
   ```

4. **Check network connectivity**:
   ```bash
   docker network ls
   docker network inspect n8n_default
   ```

## N8N MCP Client Node Settings

When configuring the MCP Client node in n8n:

1. **Server Type**: Choose "HTTP" or "WebSocket"
2. **Server URL**: Use one of the URLs listed above
3. **Authentication**: None (our server doesn't require auth)
4. **Headers**: Default (CORS is handled automatically)

## Example Tool Call

Once connected, you can call tools like:
```json
{
  "tool_name": "summarize_csv_file",
  "arguments": {
    "filename": "sample.csv"
  }
}
```

## Troubleshooting Logs

Monitor both services:
```bash
# Real-time logs
docker-compose logs -f

# MCP server only
docker-compose logs -f mcp-server

# N8N only  
docker-compose logs -f n8n
```
