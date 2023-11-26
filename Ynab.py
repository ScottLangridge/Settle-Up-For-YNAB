import requests

class Ynab:
    def __init__(self, api_token):
        self.ROOT_URL = "https://api.ynab.com/v1"

        self.api_token = api_token

    def test_connection(self):
        return self._get("/budgets").status_code == 200

    def _get(self, endpoint):
        headers = {'Authorization': f'Bearer {self.api_token}'}
        return requests.get(self.ROOT_URL + endpoint, headers=headers)
