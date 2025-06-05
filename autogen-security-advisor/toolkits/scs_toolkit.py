from typing import List, Dict, Optional
from mcp_clients.harness_client import HarnessClient

class SCSToolkit:
    def __init__(self, clients):
        self.clients = clients
    
    def get_supply_chain_risks(self, org: str, limit: int = 10) -> List[Dict]:
        """Fetch supply chain risks for the given org using harness-mcp-server."""
        harness_client = self.clients.get("harness")
        if harness_client:
            return harness_client.get_supply_chain_risks(org, limit)
        return []

    def get_most_used_oss_component(self, org: str) -> Optional[Dict]:
        """Fetch OSS components and return the most used one for the given org using harness-mcp-server."""
        harness_client = self.clients.get("harness")
        if not harness_client:
            return None
        components = harness_client.get_oss_components(org)
        if not components:
            return None
        return max(
            components.get("components", []),
            key=lambda x: x.get("usage_count", 0),
            default=None
        )
    
    def get_slsa_non_compliant_systems(self, org: str) -> List[Dict]:
        harness_client = self.clients.get("harness")
        if not harness_client:
            return []
        
        systems = harness_client.get_slsa_compliance(org)
        return [s for s in systems if not s.get("compliant", False)]
    
    def get_unsigned_artifacts(self, org: str) -> List[Dict]:
        harness_client = self.clients.get("harness")
        if harness_client:
            return harness_client.get_unsigned_artifacts(org)
        return []
    
    def download_oss_report(self, org: str, format: str = "pdf") -> Optional[bytes]:
        harness_client = self.clients.get("harness")
        if harness_client:
            return harness_client.get_oss_compliance_report(org, format)
        return None
    
    def set_slsa_enforcement(self, org: str, enforce: bool) -> bool:
        harness_client = self.clients.get("harness")
        if harness_client:
            return harness_client.enforce_slsa_compliance(org, enforce)
        return False