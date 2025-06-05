from config import Config
from agents.security_agents import SecurityAgents
from mcp_clients.github_client import GitHubClient
from mcp_clients.harness_client import HarnessClient
from toolkits.sto_toolkit import STOToolkit
from toolkits.scs_toolkit import SCSToolkit
from rag.rag_template import RAGTemplate
import autogen

def main():
    config = Config()
    
    # Initialize clients
    clients = {
        "github": GitHubClient("github", config.MCP_SERVERS["github"]),
        "harness": HarnessClient(config.MCP_SERVERS["harness"])
    }
    
    # Initialize agents
    agents = SecurityAgents(config.LLM_CONFIG)
    sto_assistant = agents.create_sto_assistant()
    scs_assistant = agents.create_scs_assistant()
    
    # Initialize RAG
    rag = RAGTemplate({
        "api_key": config.LLM_CONFIG["api_key"],
        **config.RAG_CONFIG
    })
    
    # Initialize toolkits
    sto_toolkit = STOToolkit(clients)
    scs_toolkit = SCSToolkit(clients)
    
    # Register tools
    from typing import List, Dict
    def get_top_vulnerabilities_toolkit(repos: List[str], limit: int = 10) -> List[Dict]:
        return sto_toolkit.get_top_vulnerabilities(repos, limit)

    autogen.register_function(
        get_top_vulnerabilities_toolkit,
        caller=sto_assistant,
        executor=agents.user_proxy,
        name="get_top_vulnerabilities",
        description="Fetch the top N critical vulnerabilities from MCP servers."
    )
    
    # Add similar registrations for other tools
    
    # Prompt selection UI
    STO_PROMPTS = [
        "Tell me the top 10 critical vulnerabilities most recently discovered",
        "Should I create a PR to fix them ?",
        "Should I create a policy to block them in the pipeline ?",
        "Tell me the exemptions raised by the developers that need to be reviewed",
        "Should I allow or deny these exemptions ?",
        "Tell me how did my security risk posture changed in the last 1 week",
        "Should I download a report ?"
    ]
    SCS_PROMPTS = [
        "Tell me the top 10 recent supply chain risks discovered ",
        "Tell me the most used OSS component across all builds with vulnerabilities",
        "Should I download an OSS compliance report ?",
        "Tell me which build systems are not SLSA compliant",
        "Should I enforce SLSA compliance ?",
        "Tell me which deployed artifacts are not signed ?",
        "Should I enforce artifact signing ?"
    ]
    print("Available STO Prompts:")
    for idx, p in enumerate(STO_PROMPTS, 1):
        print(f"{idx}. {p}")
    print("\nAvailable SCS Prompts:")
    for idx, p in enumerate(SCS_PROMPTS, 1):
        print(f"{idx+len(STO_PROMPTS)}. {p}")
    print(f"{len(STO_PROMPTS) + len(SCS_PROMPTS) + 1}. Custom prompt")
    
    choice = input("\nPick a prompt by number or enter your own: ")
    from agents.multi_agent_manager import MultiAgentManager
    agent_dict = {
        "STO_Specialist": sto_assistant,
        "SCS_Specialist": scs_assistant
    }
    agent_capabilities = {
        "STO_Specialist": [
            "vulnerability", "policy", "exemption", "security posture", "pr", "pipeline", "risk posture"
        ],
        "SCS_Specialist": [
            "supply chain", "oss", "dependency", "composition", "slsa", "artifact", "compliance", "unsigned", "report"
        ]
    }
    multi_agent_manager = MultiAgentManager(agent_dict, agent_capabilities)

    try:
        choice_int = int(choice)
        if 1 <= choice_int <= len(STO_PROMPTS):
            prompt = STO_PROMPTS[choice_int-1]
        elif len(STO_PROMPTS) < choice_int <= len(STO_PROMPTS) + len(SCS_PROMPTS):
            prompt = SCS_PROMPTS[choice_int-len(STO_PROMPTS)-1]
        else:
            prompt = input("Enter your custom prompt: ")
    except ValueError:
        prompt = choice

    print(f"\nSelected prompt: {prompt}")
    assistant = multi_agent_manager.select_agent(prompt)
    print(f"\nSelected assistance: {assistant.name}")
    agents.user_proxy.initiate_chat(
        assistant,
        message=prompt
    )

if __name__ == "__main__":
    main()
