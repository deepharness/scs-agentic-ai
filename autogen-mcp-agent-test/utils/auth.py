# utils/auth.py
import os

def get_auth_header() -> str:
    # e.g. load from environment or config.py
    from config import Settings
    return Settings.MCP_API_KEY
