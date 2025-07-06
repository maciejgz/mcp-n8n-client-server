#!/usr/bin/env python3
"""
Start script for MCP Mix Server
Usage:
    python start.py                    # Start as standard MCP server
    python start.py --http            # Start as HTTP server for n8n
    python start.py --docker          # Build and run in Docker
    python start.py --help            # Show help
"""

import asyncio
import subprocess
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def show_help():
    """Show help message"""
    print(__doc__)
    print("\nAvailable commands:")
    print("  --http     Start HTTP server for n8n integration (port 8000)")
    print("  --docker   Build and run in Docker container")
    print("  --help     Show this help message")

def build_docker():
    """Build Docker container"""
    logger.info("Building Docker container...")
    try:
        result = subprocess.run(
            ["docker", "build", "-t", "mix-server", "."],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logger.info("Docker container built successfully")
            return True
        else:
            logger.error(f"Docker build failed: {result.stderr}")
            return False
    except FileNotFoundError:
        logger.error("Docker not found. Please install Docker first.")
        return False

def run_docker():
    """Run Docker container"""
    logger.info("Starting Docker container...")
    try:
        subprocess.run([
            "docker", "run", "-d", 
            "--name", "mix-server-container",
            "-p", "8000:8000",
            "--rm",
            "mix-server"
        ])
        logger.info("Docker container started on port 8000")
        logger.info("You can access the server at http://localhost:8000")
        logger.info("To stop: docker stop mix-server-container")
    except Exception as e:
        logger.error(f"Failed to start Docker container: {e}")

async def start_server(http_mode=False):
    """Start the MCP server"""
    try:
        if http_mode:
            from main import create_http_server
            import uvicorn
            logger.info("Creating HTTP server for n8n integration...")
            app = await create_http_server()
            if app:
                # Use Config to avoid asyncio event loop conflict
                config = uvicorn.Config(app, host="0.0.0.0", port=8000)
                server = uvicorn.Server(config)
                await server.serve()
            else:
                logger.error("Failed to create HTTP server")
        else:
            from server import mcp
            logger.info("Starting standard MCP server...")
            # Use mcp.run() directly, it handles its own event loop
            mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--help":
            show_help()
            return
            
        elif command == "--docker":
            if build_docker():
                run_docker()
            return
            
        elif command == "--http":
            logger.info("Starting HTTP server for n8n...")
            asyncio.run(start_server(http_mode=True))
            return
            
        else:
            logger.error(f"Unknown command: {command}")
            show_help()
            return
    
    # Default: start as standard MCP server
    logger.info("Starting standard MCP server...")
    # For standard MCP server, don't use asyncio.run since mcp.run() handles its own event loop
    from server import mcp
    mcp.run()

if __name__ == "__main__":
    main()
