import requests
from .base_client import MCPClient

class GitHubClient(MCPClient):
    def __init__(self, server_type, config):
        super().__init__(server_type, config)

    def get_dependabot_alerts(self, owner, repo):
        url = f"{self.base_url}/repos/{owner}/{repo}/dependabot/alerts"
        headers = self.headers.copy()
        headers["Accept"] = "application/vnd.github+json"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch dependabot alerts: {response.status_code} - {response.text}")
            return []

    def get_security_advisories(self, org):
        url = f"{self.base_url}/orgs/{org}/security-advisories"
        headers = self.headers.copy()
        headers["Accept"] = "application/vnd.github+json"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch security advisories: {response.status_code} - {response.text}")
            return []

    def get_repo_vulnerabilities(self, owner, repo):
        # GitHub does not have a direct REST endpoint for all vulnerabilities, use dependabot alerts or advisories
        return self.get_dependabot_alerts(owner, repo)

    def get_critical_vulnerabilities(self, repos=None, org=None, limit=10):
        """
        Fetch the top critical vulnerabilities from the native GitHub REST API by looping over repos and using /dependabot/alerts.
        If repos is None, load from the environment variable GITHUB_REPOS (comma-separated), or fallback to config if available.
        """
        import os
        results = []
        if repos is None:
            env_repos = os.environ.get("GITHUB_REPOS")
            if env_repos:
                repos = [r.strip() for r in env_repos.split(",") if r.strip()]
            else:
                # Optionally fallback to config.REPOS if available
                repos = getattr(self, "default_repos", [])
            if not repos:
                print("No repositories provided for vulnerability search (repos argument, GITHUB_REPOS env, or config.REPOS).")
                return []
        for repo_full_name in repos:
            try:
                owner, repo = repo_full_name.split('/')
            except ValueError:
                print(f"Repo name '{repo_full_name}' is not in 'owner/repo' format. Skipping.")
                continue
            url = f"{self.base_url}/repos/{owner}/{repo}/dependabot/alerts"
            headers = self.headers.copy()
            headers["Accept"] = "application/vnd.github+json"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                alerts = response.json()
                crit_alerts = [a for a in alerts if a.get("security_advisory", {}).get("severity") == "critical"]
                results.extend(crit_alerts)
                if len(results) >= limit:
                    break
            else:
                print(f"Failed to fetch dependabot alerts for {repo_full_name}: {response.status_code} - {response.text}")
        return results[:limit]

    # Add more methods as needed for exemptions, PRs, etc.
