# agent.py
import os
from dotenv import load_dotenv
from autogen import AutogenAgent, OpenAIAssistantConfig
from mcp_tool_loader import MCPToolLoader
from config import Settings

# 1. Optionally load environment variables from a local ".env" file
load_dotenv()

def main():
    # 2. Create the MCPToolLoader, which under the hood will do GET /.well-known/mcp/manifest.json
    loader = MCPToolLoader(
        base_url=Settings.MCP_BASE_URL,
        authorization_header=Settings.MCP_API_KEY,
    )

    # 3. Load all tools
    tools = loader.load_tools()

    # 4. Create the LLM assistant + agent
    assistant_cfg = OpenAIAssistantConfig(model_name="gpt-4o-mini")
    agent = AutogenAgent(
        assistant_config=assistant_cfg,
        tools=tools,
    )

    # 5. Example: run a single tool by name
    result = agent.run_tool(
        tool_name="get_top_vulnerabilities",
        args={"repo": "acme/my-repo", "limit": 5},
    )
    print("get_top_vulnerabilities →", result)

    # 6. (Optional) Kick off a chat/plan loop:
    # response = agent.run("List top 3 supply-chain risks for acme/my-repo.")
    # print("Agent replied:", response)

if __name__ == "__main__":
    main()
