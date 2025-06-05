import os
import json
from mcp_clients.github_client import GitHubClient
from mcp_clients.harness_client import HarnessClient
from llm.base import get_llm
from prompts.sto import STO_PROMPTS
from prompts.scs import SCS_PROMPTS
from rag.rag_template import RAGTemplate

# Initialize MCP clients
github = GitHubClient()
harness = HarnessClient()

# Initialize LLM (pluggable)
config_path = os.path.join(os.path.dirname(__file__), "config.json")
openai_api_key = None
if os.path.exists(config_path):
    with open(config_path) as f:
        config = json.load(f)
        openai_api_key = config.get("openai_api_key")
if not openai_api_key:
    openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("ERROR: Please set the OPENAI_API_KEY environment variable or add it to config.json.")
    exit(1)
llm = get_llm(api_key=openai_api_key)

# Example: Fetch data and answer a prompt
def answer_prompt(prompt):
    context = RAGTemplate.select_context(prompt, github, harness)
    return llm.answer(prompt, context)

if __name__ == "__main__":
    print("Available STO Prompts:")
    for p in STO_PROMPTS:
        print("-", p)
    print("\nAvailable SCS Prompts:")
    for p in SCS_PROMPTS:
        print("-", p)
    # Example interactive loop
    user_prompt = input("\nEnter your prompt: ")
    print("\nAnswer:")
    print(answer_prompt(user_prompt))
