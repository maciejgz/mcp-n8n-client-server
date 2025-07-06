# main.py
import asyncio
import logging
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server
from mcp.server import Server
from mcp.types import Tool, TextContent
import json

import tools.csv_tools
import tools.parquet_tools

from server import mcp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HTTP server wrapper for n8n integration
class MCPHTTPWrapper:
    """HTTP wrapper for MCP server to integrate with n8n"""
    
    def __init__(self, mcp_server: FastMCP):
        self.mcp_server = mcp_server
    
    async def handle_tool_call(self, tool_name: str, arguments: dict) -> dict:
        """Handle tool calls from n8n"""
        try:
            # Get available tools
            tools_response = await self.mcp_server.list_tools()
            
            # Handle both list and object with tools attribute
            if hasattr(tools_response, 'tools'):
                tools_list = tools_response.tools
            else:
                tools_list = tools_response
            
            # Find the requested tool
            tool = next((t for t in tools_list if t.name == tool_name), None)
            if not tool:
                raise ValueError(f"Tool '{tool_name}' not found")
            
            # Call the tool
            result = await self.mcp_server.call_tool(tool_name, arguments)
            
            # Handle different result formats
            if hasattr(result, 'content') and result.content:
                result_text = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
            elif isinstance(result, tuple) and len(result) > 0:
                # Extract text from tuple containing TextContent objects
                content_list = result[0] if isinstance(result[0], list) else [result[0]]
                if content_list and hasattr(content_list[0], 'text'):
                    result_text = content_list[0].text
                else:
                    result_text = str(result)
            else:
                result_text = str(result)
            
            return {
                "success": True,
                "result": result_text,
                "tool_name": tool_name
            }
            
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "tool_name": tool_name
            }

# Create HTTP server using FastAPI
async def create_http_server():
    """Create HTTP server for n8n integration"""
    try:
        from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
        from fastapi.middleware.cors import CORSMiddleware
        from pydantic import BaseModel
        import uvicorn
        
        app = FastAPI(title="MCP Server for n8n", version="1.0.0")
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        wrapper = MCPHTTPWrapper(mcp)
        
        class ToolCallRequest(BaseModel):
            tool_name: str
            arguments: dict = {}
        
        @app.get("/health")
        async def health_check():
            logger.info("Health check requested")
            return {"status": "healthy", "server": "MCP Mix Server", "timestamp": asyncio.get_event_loop().time()}
        
        @app.get("/tools")
        async def list_tools():
            """List available tools"""
            try:
                tools_response = await mcp.list_tools()
                # Handle both list and object with tools attribute
                if hasattr(tools_response, 'tools'):
                    tools_list = tools_response.tools
                else:
                    tools_list = tools_response
                
                return {
                    "tools": [
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.inputSchema
                        }
                        for tool in tools_list
                    ]
                }
            except Exception as e:
                logger.error(f"Error listing tools: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/n8n")
        async def n8n_endpoint():
            """Simple endpoint for n8n MCP integration"""
            logger.info("N8N endpoint called")
            try:
                tools_response = await mcp.list_tools()
                if hasattr(tools_response, 'tools'):
                    tools_list = tools_response.tools
                else:
                    tools_list = tools_response
                
                response = {
                    "serverInfo": {
                        "name": "MCP Mix Server",
                        "version": "1.0.0"
                    },
                    "capabilities": {
                        "tools": {}
                    },
                    "tools": [
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "inputSchema": tool.inputSchema
                        }
                        for tool in tools_list
                    ]
                }
                logger.info(f"N8N response: {len(tools_list)} tools available")
                return response
            except Exception as e:
                logger.error(f"N8N endpoint error: {str(e)}", exc_info=True)
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/test-connection")
        async def test_connection():
            """Test endpoint for n8n connection debugging"""
            logger.info("Test connection endpoint called")
            try:
                tools_response = await mcp.list_tools()
                if hasattr(tools_response, 'tools'):
                    tools_list = tools_response.tools
                else:
                    tools_list = tools_response
                
                return {
                    "status": "success",
                    "message": "MCP server is running and accessible",
                    "server": "MCP Mix Server",
                    "version": "1.0.0",
                    "tools_count": len(tools_list),
                    "tools": [tool.name for tool in tools_list],
                    "timestamp": asyncio.get_event_loop().time()
                }
            except Exception as e:
                logger.error(f"Test connection error: {str(e)}", exc_info=True)
                return {
                    "status": "error",
                    "message": str(e),
                    "timestamp": asyncio.get_event_loop().time()
                }
        
        @app.post("/call-tool")
        async def call_tool(request: ToolCallRequest):
            """Call a specific tool"""
            result = await wrapper.handle_tool_call(request.tool_name, request.arguments)
            if not result["success"]:
                raise HTTPException(status_code=400, detail=result["error"])
            return result
        
        @app.get("/sse")
        async def sse_endpoint():
            """Standard MCP SSE endpoint for protocol communication"""
            from fastapi.responses import StreamingResponse
            from fastapi import Request
            import json
            
            async def event_generator():
                try:
                    # Send server capabilities
                    capabilities = {
                        "jsonrpc": "2.0",
                        "method": "notifications/initialized",
                        "params": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {
                                "tools": {},
                                "logging": {},
                                "prompts": {}
                            },
                            "serverInfo": {
                                "name": "MCP Mix Server",
                                "version": "1.0.0"
                            }
                        }
                    }
                    yield f"data: {json.dumps(capabilities)}\n\n"
                    
                    # Send available tools
                    tools_response = await mcp.list_tools()
                    if hasattr(tools_response, 'tools'):
                        tools_list = tools_response.tools
                    else:
                        tools_list = tools_response
                    
                    tools_message = {
                        "jsonrpc": "2.0",
                        "method": "notifications/tools/list_changed",
                        "params": {
                            "tools": [
                                {
                                    "name": tool.name,
                                    "description": tool.description,
                                    "inputSchema": tool.inputSchema
                                }
                                for tool in tools_list
                            ]
                        }
                    }
                    yield f"data: {json.dumps(tools_message)}\n\n"
                    
                    # Keep connection alive with heartbeat
                    while True:
                        await asyncio.sleep(30)
                        heartbeat = {
                            "jsonrpc": "2.0",
                            "method": "notifications/progress",
                            "params": {
                                "progressToken": "heartbeat",
                                "value": {
                                    "kind": "report",
                                    "message": "Server alive"
                                }
                            }
                        }
                        yield f"data: {json.dumps(heartbeat)}\n\n"
                        
                except Exception as e:
                    logger.error(f"SSE error: {str(e)}")
                    error_message = {
                        "jsonrpc": "2.0",
                        "method": "notifications/error",
                        "params": {
                            "error": {
                                "code": -32603,
                                "message": str(e)
                            }
                        }
                    }
                    yield f"data: {json.dumps(error_message)}\n\n"
            
            return StreamingResponse(
                event_generator(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*",
                }
            )
        
        @app.get("/mcp")
        async def mcp_get_endpoint():
            """MCP GET endpoint for initialization"""
            logger.info("MCP GET endpoint called")
            try:
                tools_response = await mcp.list_tools()
                if hasattr(tools_response, 'tools'):
                    tools_list = tools_response.tools
                else:
                    tools_list = tools_response
                
                response = {
                    "jsonrpc": "2.0",
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "MCP Mix Server",
                            "version": "1.0.0"
                        },
                        "tools": [
                            {
                                "name": tool.name,
                                "description": tool.description,
                                "inputSchema": tool.inputSchema
                            }
                            for tool in tools_list
                        ]
                    }
                }
                logger.info(f"MCP GET response: {len(tools_list)} tools available")
                return response
            except Exception as e:
                logger.error(f"MCP GET endpoint error: {str(e)}", exc_info=True)
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
        
        @app.post("/mcp")
        async def mcp_post_endpoint(request: dict):
            """MCP POST endpoint for tool calls"""
            try:
                # Handle POST requests
                if request.get("method") == "tools/list":
                    tools_response = await mcp.list_tools()
                    if hasattr(tools_response, 'tools'):
                        tools_list = tools_response.tools
                    else:
                        tools_list = tools_response
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {
                            "tools": [
                                {
                                    "name": tool.name,
                                    "description": tool.description,
                                    "inputSchema": tool.inputSchema
                                }
                                for tool in tools_list
                            ]
                        }
                    }
                
                elif request.get("method") == "tools/call":
                    params = request.get("params", {})
                    tool_name = params.get("name")
                    arguments = params.get("arguments", {})
                    
                    result = await wrapper.handle_tool_call(tool_name, arguments)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": result.get("result", "")
                                }
                            ]
                        }
                    }
                
                else:
                    raise HTTPException(status_code=400, detail=f"Unknown method: {request.get('method')}")
                    
            except Exception as e:
                logger.error(f"MCP POST endpoint error: {str(e)}")
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id") if request else None,
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
        
        @app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for MCP protocol"""
            logger.info("WebSocket connection attempt")
            await websocket.accept()
            try:
                while True:
                    # Receive JSON-RPC message
                    data = await websocket.receive_text()
                    logger.info(f"WebSocket received: {data}")
                    
                    try:
                        request = json.loads(data)
                        
                        # Handle MCP protocol messages
                        if request.get("method") == "initialize":
                            response = {
                                "jsonrpc": "2.0",
                                "id": request.get("id"),
                                "result": {
                                    "protocolVersion": "2024-11-05",
                                    "capabilities": {
                                        "tools": {}
                                    },
                                    "serverInfo": {
                                        "name": "MCP Mix Server",
                                        "version": "1.0.0"
                                    }
                                }
                            }
                            await websocket.send_text(json.dumps(response))
                            
                        elif request.get("method") == "tools/list":
                            tools_response = await mcp.list_tools()
                            if hasattr(tools_response, 'tools'):
                                tools_list = tools_response.tools
                            else:
                                tools_list = tools_response
                            
                            response = {
                                "jsonrpc": "2.0",
                                "id": request.get("id"),
                                "result": {
                                    "tools": [
                                        {
                                            "name": tool.name,
                                            "description": tool.description,
                                            "inputSchema": tool.inputSchema
                                        }
                                        for tool in tools_list
                                    ]
                                }
                            }
                            await websocket.send_text(json.dumps(response))
                            
                        elif request.get("method") == "tools/call":
                            params = request.get("params", {})
                            tool_name = params.get("name")
                            arguments = params.get("arguments", {})
                            
                            result = await wrapper.handle_tool_call(tool_name, arguments)
                            
                            response = {
                                "jsonrpc": "2.0",
                                "id": request.get("id"),
                                "result": {
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": result.get("result", "")
                                        }
                                    ]
                                }
                            }
                            await websocket.send_text(json.dumps(response))
                            
                        else:
                            # Unknown method
                            error_response = {
                                "jsonrpc": "2.0",
                                "id": request.get("id"),
                                "error": {
                                    "code": -32601,
                                    "message": f"Method not found: {request.get('method')}"
                                }
                            }
                            await websocket.send_text(json.dumps(error_response))
                            
                    except json.JSONDecodeError:
                        error_response = {
                            "jsonrpc": "2.0",
                            "error": {
                                "code": -32700,
                                "message": "Parse error"
                            }
                        }
                        await websocket.send_text(json.dumps(error_response))
                        
            except WebSocketDisconnect:
                logger.info("WebSocket disconnected")
            except Exception as e:
                logger.error(f"WebSocket error: {str(e)}", exc_info=True)
        
        return app
        
    except ImportError:
        logger.error("FastAPI not installed. Install with: pip install fastapi uvicorn")
        return None

# Entry point to run the server
def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        # Run as HTTP server for n8n
        logger.info("Starting HTTP server for n8n integration...")
        async def run_http():
            app = await create_http_server()
            if app:
                import uvicorn
                # Use Config to avoid asyncio event loop conflict
                config = uvicorn.Config(app, host="0.0.0.0", port=8000)
                server = uvicorn.Server(config)
                await server.serve()
            else:
                logger.error("Failed to create HTTP server")
        
        asyncio.run(run_http())
    else:
        # Run as standard MCP server
        logger.info("Starting MCP server...")
        # Use mcp.run() directly without asyncio.run since it handles its own event loop
        mcp.run()

if __name__ == "__main__":
    main()