# mcp_tool_loader.py
import requests
from autogen import Tool
from autogen_mcp import MCPToolLoader as _RawMCPToolLoader  # rename to avoid confusion

class MCPToolLoader:
    def __init__(self, base_url: str, authorization_header: str):
        self.base_url = base_url.rstrip("/")  # e.g. "http://localhost:8080"
        self.authorization = authorization_header

    def load_tools(self) -> list[Tool]:
        # Delegate to the autogen_mcp package, which handles fetching the manifest
        raw_loader = _RawMCPToolLoader(
            base_url=self.base_url,
            authorization_header=self.authorization,
        )
        return raw_loader.load_tools()
