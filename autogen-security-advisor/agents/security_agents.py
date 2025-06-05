from autogen import AssistantAgent, UserProxyAgent

class SecurityAgents:
    def __init__(self, llm_config):
        self.llm_config = llm_config
        self.user_proxy = UserProxyAgent(
            name="User_Proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=5,
            code_execution_config={
                "work_dir": "coding",
                "use_docker": False
            }
        )
    
    def create_sto_assistant(self):
        return AssistantAgent(
            name="STO_Specialist",
            system_message=self._get_sto_system_prompt(),
            llm_config=self.llm_config
        )
    
    def create_scs_assistant(self):
        return AssistantAgent(
            name="SCS_Specialist",
            system_message=self._get_scs_system_prompt(),
            llm_config=self.llm_config
        )
    
    def _get_sto_system_prompt(self):
        return """You are a Security Testing Orchestration expert. Capabilities:
        - Analyze vulnerability data from MCP servers
        - Recommend PR creation for critical vulnerabilities
        - Evaluate policy creation needs
        - Review and assess exemption requests
        - Generate security posture reports"""
    
    def _get_scs_system_prompt(self):
        return """You are a Software Composition Security expert. Capabilities:
        - Identify supply chain risks in dependencies
        - Analyze OSS component usage
        - Evaluate SLSA compliance
        - Verify artifact signatures
        - Generate compliance reports"""
