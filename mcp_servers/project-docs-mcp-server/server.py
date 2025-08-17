import argparse
import os
from typing import Dict, Any

from fastmcp import FastMCP

# Create MCP server
mcp = FastMCP(
    name="ProjectDocsMCPServer",
    dependencies={"pdf": "PyPDF2"}
)


def _get_requirements() -> Dict[str, Any]:
    """
    Fetch content of PDF files stored in catalog ./private-resources/ and return
    it as a JSON where name of the file is the key and content is the value.
    """
    import glob

    pdf_dir = os.path.join(os.path.dirname(__file__), "private-resources")
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    result = {}
    from PyPDF2 import PdfReader

    for pdf_path in pdf_files:
        file_name = os.path.basename(pdf_path)
        try:
            with open(pdf_path, "rb") as f:
                reader = PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
            result[file_name] = text
        except Exception as e:
            result[file_name] = f"Error reading file: {e}"
    return result


@mcp.tool("get_requirements")
def get_requirements_tool() -> str:
    """
    Get the requirements for the IT project which is under development.
    Use it always when user asks for analysing developed projects and its
    alignment with business goals and analysis or just for the requirements.
    """
    requirements = _get_requirements()
    return str(requirements)


@mcp.resource("data://requirements")
def get_requirements() -> str:
    """
    Get the requirements for the IT project which is under development.
    Use it always when user asks for analysing developed projects and its
    alignment with business goals and analysis or just for the requirements.
    """
    requirements = _get_requirements()
    return str(requirements)


def test_get_requirements():
    """
    Simple test for get_requirements. Prints result for the project requirements.
    """
    print("Testing get_requirements")
    result = _get_requirements()
    print("Result:", result)


def main():
    parser = argparse.ArgumentParser(description="Weather MCP Server")
    parser.add_argument("--http", action="store_true", help="Run as HTTP server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8001, help="Port to bind to")
    parser.add_argument(
        "--test", action="store_true", help="Run test for get_requirements"
    )
    args = parser.parse_args()
    if args.test:
        test_get_requirements()
        return
    if args.http:
        print("Starting HTTP MCP server...")
        mcp.run(transport="http", host=args.host, port=args.port)
    else:
        print("Starting stdio MCP server...")
        mcp.run()


if __name__ == "__main__":
    main()
