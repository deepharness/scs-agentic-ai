import requests
from typing import List, Dict, Any, Optional
from .base_client import MCPClient

class HarnessClient(MCPClient):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("harness", config)
        # Harness requires account ID in headers
        self.headers.update({"Harness-Account": config.get("account_id", "")})
    
    def get_supply_chain_risks(self, org: str, limit: int = 10) -> List[Dict]:
        """Get recent supply chain risks from Harness SCS"""
        endpoint = "scs/risks"
        params = {
            "org": org,
            "limit": limit,
            "sort": "timestamp",
            "order": "desc"
        }
        response = self.fetch_data(endpoint, params)
        return response.get("risks", [])[:limit] if response else []
    
    def get_oss_components(self, org: str) -> Dict[str, Any]:
        """Get OSS components with vulnerability data"""
        endpoint = "scs/oss/components"
        params = {"org": org}
        return self.fetch_data(endpoint, params) or {}
    
    def get_slsa_compliance(self, org: str) -> List[Dict]:
        """Get build systems and their SLSA compliance status"""
        endpoint = "build/slsa"
        params = {"org": org}
        return self.fetch_data(endpoint, params) or []
    
    def get_unsigned_artifacts(self, org: str) -> List[Dict]:
        """Get deployed artifacts that are not signed"""
        endpoint = "deployments/unsigned"
        params = {"org": org}
        return self.fetch_data(endpoint, params) or []
    
    def get_oss_compliance_report(self, org: str, format: str = "pdf") -> Optional[bytes]:
        """Download OSS compliance report"""
        endpoint = f"scs/reports/oss-compliance.{format}"
        params = {"org": org}
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error downloading report: {str(e)}")
            return None
    
    def enforce_slsa_compliance(self, org: str, enforce: bool = True) -> bool:
        """Enable/disable SLSA compliance enforcement"""
        endpoint = "policies/slsa"
        payload = {
            "org": org,
            "enforce": enforce
        }
        try:
            response = requests.post(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                json=payload,
                timeout=10
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
