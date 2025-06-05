from typing import Dict, List

class MultiAgentManager:
    """
    Dynamically selects the most appropriate agent based on declared capabilities and the user prompt.
    """
    def __init__(self, agents: Dict[str, object], capabilities: Dict[str, List[str]]):
        """
        agents: Dict of agent_name -> agent_instance
        capabilities: Dict of agent_name -> list of capability keywords/phrases
        """
        self.agents = agents
        self.capabilities = capabilities

    def select_agent(self, prompt: str):
        prompt_lower = prompt.lower()
        best_agent = None
        best_score = 0
        for agent_name, keywords in self.capabilities.items():
            score = sum(1 for word in keywords if word in prompt_lower)
            if score > best_score:
                best_score = score
                best_agent = agent_name
        # Fallback to first agent if no match
        if best_agent is None:
            best_agent = list(self.agents.keys())[0]
        return self.agents[best_agent]
