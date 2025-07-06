#!/usr/bin/env python3
"""
Test script for MCP Mix Server
Tests both MCP functionality and HTTP API
"""

import asyncio
import json
import logging
import requests
import time
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MCPServerTester:
    """Test class for MCP server functionality"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        
    def test_health_check(self):
        """Test server health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                logger.info("✓ Health check passed")
                return True
            else:
                logger.error(f"✗ Health check failed: {response.status_code}")
                return False
        except requests.RequestException as e:
            logger.error(f"✗ Health check failed: {e}")
            return False
    
    def test_list_tools(self):
        """Test listing available tools"""
        try:
            response = requests.get(f"{self.base_url}/tools", timeout=5)
            if response.status_code == 200:
                tools = response.json()
                logger.info(f"✓ Found {len(tools.get('tools', []))} tools")
                for tool in tools.get('tools', []):
                    logger.info(f"  - {tool['name']}: {tool['description']}")
                return True
            else:
                logger.error(f"✗ List tools failed: {response.status_code}")
                return False
        except requests.RequestException as e:
            logger.error(f"✗ List tools failed: {e}")
            return False
    
    def test_csv_tool(self):
        """Test CSV summarization tool"""
        try:
            payload = {
                "tool_name": "summarize_csv_file",
                "arguments": {
                    "filename": "sample.csv"
                }
            }
            
            response = requests.post(
                f"{self.base_url}/call-tool",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info(f"✓ CSV tool test passed: {result.get('result')}")
                    return True
                else:
                    logger.error(f"✗ CSV tool test failed: {result.get('error')}")
                    return False
            else:
                logger.error(f"✗ CSV tool test failed: {response.status_code} - {response.text}")
                return False
                
        except requests.RequestException as e:
            logger.error(f"✗ CSV tool test failed: {e}")
            return False
    
    def test_parquet_tool(self):
        """Test Parquet summarization tool"""
        try:
            payload = {
                "tool_name": "summarize_parquet_file",
                "arguments": {
                    "filename": "sample.parquet"
                }
            }
            
            response = requests.post(
                f"{self.base_url}/call-tool",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info(f"✓ Parquet tool test passed: {result.get('result')}")
                    return True
                else:
                    logger.error(f"✗ Parquet tool test failed: {result.get('error')}")
                    return False
            else:
                logger.error(f"✗ Parquet tool test failed: {response.status_code} - {response.text}")
                return False
                
        except requests.RequestException as e:
            logger.error(f"✗ Parquet tool test failed: {e}")
            return False
    
    def test_invalid_tool(self):
        """Test calling non-existent tool"""
        try:
            payload = {
                "tool_name": "non_existent_tool",
                "arguments": {}
            }
            
            response = requests.post(
                f"{self.base_url}/call-tool",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 400:
                logger.info("✓ Invalid tool test passed (correctly rejected)")
                return True
            else:
                logger.error(f"✗ Invalid tool test failed: Expected 400, got {response.status_code}")
                return False
                
        except requests.RequestException as e:
            logger.error(f"✗ Invalid tool test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        logger.info("Starting MCP Server tests...")
        logger.info("=" * 50)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("List Tools", self.test_list_tools),
            ("CSV Tool", self.test_csv_tool),
            ("Parquet Tool", self.test_parquet_tool),
            ("Invalid Tool", self.test_invalid_tool)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            logger.info(f"\nRunning {test_name}...")
            if test_func():
                passed += 1
            time.sleep(1)  # Small delay between tests
        
        logger.info("=" * 50)
        logger.info(f"Tests completed: {passed}/{total} passed")
        
        if passed == total:
            logger.info("🎉 All tests passed! Server is ready for n8n integration.")
        else:
            logger.warning(f"⚠️  {total - passed} test(s) failed. Check server configuration.")
        
        return passed == total

def wait_for_server(base_url, max_wait=30):
    """Wait for server to be ready"""
    logger.info(f"Waiting for server at {base_url}...")
    
    for i in range(max_wait):
        try:
            response = requests.get(f"{base_url}/health", timeout=2)
            if response.status_code == 200:
                logger.info("Server is ready!")
                return True
        except requests.RequestException:
            pass
        
        if i < max_wait - 1:
            time.sleep(1)
    
    logger.error("Server did not start within the timeout period")
    return False

def main():
    """Main test function"""
    import sys
    
    base_url = "http://localhost:8000"
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print(__doc__)
            print("\nUsage:")
            print("  python test_server.py           # Test server at localhost:8000")
            print("  python test_server.py --wait    # Wait for server then test")
            print("  python test_server.py --help    # Show this help")
            return
        elif sys.argv[1] == "--wait":
            if not wait_for_server(base_url):
                return
    
    # Run tests
    tester = MCPServerTester(base_url)
    tester.run_all_tests()

if __name__ == "__main__":
    main()
