import requests
import curlify
import json

class Ynab:
    def __init__(self, api_token):
        self.ROOT_URL = 'https://api.ynab.com/v1'

        self.api_token = api_token
        self._test_connection()
        self.budget_id = self._get_budget_id()

    def get_transactions(self):
        endpoint = f'/budgets/{self.budget_id}/transactions'
        return self._get(endpoint)['transactions']

    #  Expected params and their nullabilities can be found at Request body > Scheme here:
    #  https://api.ynab.com/v1#/Transactions/createTransaction
    #
    #  Note that account_id is handled automatically below
    def create_transaction(self, params):
        endpoint = f'/budgets/{self.budget_id}/transactions'
        return self._post(endpoint, params)

    def get_accounts(self):
        return self._get(f'/budgets/{self.budget_id}/accounts')['accounts']

    def _get_budget_id(self):
        budgets = self._get('/budgets')['budgets']

        # Implement OAuth to if more than one budget exists. See https://api.ynab.com/#oauth-default-budget
        assert len(budgets) == 1, 'YNAB API Accessor currently only supports accounts with one budget'
        return budgets[0]['id']

    def _test_connection(self):
        endpoint = '/budgets'
        headers = {'Authorization': f'Bearer {self.api_token}'}
        assert requests.get(self.ROOT_URL + endpoint, headers=headers).ok, 'Ynab._test_connection failed'

    def _get(self, endpoint, params=None):
        if params is None:
            params = {}
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_token}'
        }
        response = requests.get(self.ROOT_URL + endpoint, headers=headers, data=json.dumps(params))
        assert response.ok, f'Response to GET had status code {response.status_code}\nRequest: {curlify.to_curl(response.request)}\nResponse: {response.content}'
        return response.json()['data']

    def _post(self, endpoint, params=None):
        if params is None:
            params = {}
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_token}'
        }
        response = requests.post(self.ROOT_URL + endpoint, headers=headers, data=json.dumps(params))
        assert response.ok, f'Response to GET had status code {response.status_code}\nRequest: {curlify.to_curl(response.request)}'
        return response.json()['data']
