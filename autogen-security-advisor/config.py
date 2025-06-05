import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MCP_SERVERS = {
        "github": {
            "api_key": os.getenv("GITHUB_API_KEY"),
            "base_url": "https://api.github.com"
        },
        "harness": {
            "api_key": os.getenv("HARNESS_API_KEY"),
            "base_url": "http://localhost:8080"
        }
    }
    
    LLM_CONFIG = {
        "model": "gpt-4-turbo",
        "api_key": os.getenv("OPENAI_API_KEY"),
        "temperature": 0.3,
        "timeout": 60
    }
    
    RAG_CONFIG = {
        "vector_db_path": "./rag/vector_store",
        "chunk_size": 1024
    }
    
    REPOS = ["org/repo1", "org/repo2"]
    ORGS = ["my_org"]
