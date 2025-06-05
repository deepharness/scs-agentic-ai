# config.py
import os

class Settings:
    MCP_BASE_URL: str = os.getenv("MCP_BASE_URL", "http://localhost:8080")
    MCP_API_KEY: str = os.getenv("MCP_API_KEY", "Bearer your-token-here")
