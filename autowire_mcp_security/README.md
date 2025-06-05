# Autowire MCP Security

A Python project using autowire for connecting to multiple MCP servers (GitHub, Harness) to fetch security and supply chain risk data, and answer pre-listed queries using a pluggable LLM module.

## Features
- Connects to GitHub and Harness for security data
- Answers STO and SCS security prompts
- Pluggable LLM module (OpenAI, Azure, etc.)
- RAG (Retrieval-Augmented Generation) template for context selection

## Directory Structure
```
autowire_mcp_security/
├── mcp_clients/      # Connectors for GitHub, Harness, etc.
├── prompts/          # Pre-listed prompts
├── llm/              # Pluggable LLM interface
├── rag/              # RAG template and context selectors
├── main.py           # Entry point
├── requirements.txt  # Dependencies
```

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python main.py`

## Extending LLM
Implement a new class in `llm/` and register it in `main.py`.

## Adding MCPs
Add new connectors in `mcp_clients/` following the existing pattern.
