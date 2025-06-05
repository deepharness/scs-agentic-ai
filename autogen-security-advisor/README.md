# autogen-security-advisor

## Directory Structure

```
autogen-security-advisor/
├── .env.example
├── requirements.txt
├── main.py
├── config.py
├── agents/
│   ├── __init__.py
│   ├── security_agents.py
├── mcp_clients/
│   ├── __init__.py
│   ├── base_client.py
│   ├── github_client.py
│   └── harness_client.py
├── toolkits/
│   ├── __init__.py
│   ├── sto_toolkit.py
│   └── scs_toolkit.py
├── rag/
│   ├── __init__.py
│   ├── rag_template.py
│   └── vector_store/ (auto-created at runtime)
├── data/
│   └── sample_context/ (for RAG documents)
└── utils/
    ├── __init__.py
    └── logger.py
```

## Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```
GITHUB_API_KEY=your_github_token
HARNESS_API_KEY=your_harness_token
OPENAI_API_KEY=your_openai_key
HARNESS_ACCOUNT_ID=your_harness_account_id
```

- `GITHUB_API_KEY`: GitHub personal access token with repo/security access
- `HARNESS_API_KEY`: Harness API key
- `OPENAI_API_KEY`: OpenAI API key for LLM and embeddings
- `HARNESS_ACCOUNT_ID`: Your Harness account ID

Be sure to keep your `.env` file secure and **never commit it to version control**.
