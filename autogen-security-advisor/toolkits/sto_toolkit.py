from typing import List, Dict, Optional

class STOToolkit:
    def __init__(self, clients):
        self.clients = clients
    
    def get_top_vulnerabilities(self, repos: List[str], limit: int = 10) -> List[Dict]:
        harness_client = self.clients.get("harness")
        if harness_client:
            # Replace with actual harness client method if available
            vulns = harness_client.get_critical_vulnerabilities(repos=repos, limit=limit)
            if vulns:
                return vulns[:limit]
        # Fallback: return dummy data for demo
        return [
            {"id": i, "severity": "critical", "description": f"Demo critical vulnerability {i}"}
            for i in range(1, limit+1)
        ]

    def get_exemptions(self, artifact_ids: List[str]) -> List[Dict]:
        harness_client = self.clients.get("harness")
        exemptions = []
        if harness_client:
            for artifact_id in artifact_ids:
                results = harness_client.list_compliance_results(artifact_id=artifact_id)
                # Filter for exemptions if needed, or return all results
                exemptions.extend([r for r in results if r.get("status") == "EXEMPTED"])
        return exemptions

    def get_risk_posture_change(self, repo_identifier: str) -> Optional[Dict]:
        harness_client = self.clients.get("harness")
        if harness_client:
            overview = harness_client.get_code_repo_overview(repo_identifier=repo_identifier)
            # Extract and return relevant risk posture info
            return overview.get("risk_posture") if overview else None
        return None
