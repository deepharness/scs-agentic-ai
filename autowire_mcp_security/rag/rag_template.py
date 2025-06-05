class RAGTemplate:
    @staticmethod
    def select_context(prompt, github_client, harness_client):
        # Basic template: select relevant context from MCPs based on prompt
        if "vulnerabilities" in prompt.lower():
            gh_data = github_client.fetch_critical_vulnerabilities()
            h_data = harness_client.fetch_critical_vulnerabilities()
            return f"GitHub: {gh_data}\nHarness: {h_data}"
        if "exemptions" in prompt.lower():
            gh_data = github_client.fetch_exemptions()
            h_data = harness_client.fetch_exemptions()
            return f"GitHub: {gh_data}\nHarness: {h_data}"
        # Add more context selection logic as needed
        return "No relevant context found."
