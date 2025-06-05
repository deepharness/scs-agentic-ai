import requests

class MCPClient:
    def __init__(self, server_type, config):
        self.config = config
        self.base_url = config["base_url"]
        self.headers = {"Authorization": f"Bearer {config['api_key']}"}
        self.server_type = server_type

    def fetch_data(self, endpoint, params=None):
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                params=params or {},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {self.server_type}: {str(e)}")
            return None
