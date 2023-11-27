from secrets import SECRETS
from ynab import Ynab
from datetime import datetime


class User:
    def __init__(self, secrets_id):
        self.secrets_id = secrets_id
        self.name = SECRETS[secrets_id]['name']
        self.ynab = Ynab(SECRETS[secrets_id]['token'])
        self.default_account_id = self._get_default_account_id()

    def get_transactions_since_last_settled(self):
        transactions = self.ynab.get_transactions()
        transactions_since_last_settled = []
        for i in transactions[::-1]:
            if i['flag_color'] == 'red':
                transactions_since_last_settled.append(i)
            elif i['flag_color'] == 'blue':
                break
        return transactions_since_last_settled

    def create_settle_up_transaction(self, their_name, my_subtransactions, their_subtransactions):
        amount = 0
        subtransactions = []
        for subtransaction in my_subtransactions:
            amount -= subtransaction['amount'] // 2
            subtransactions.append({
                'amount': -(subtransaction['amount'] // 2),
                'payee_name': subtransaction['payee_name']
            })
        for subtransaction in their_subtransactions:
            amount += subtransaction['amount'] // 2
            subtransactions.append({
                'amount': subtransaction['amount'] // 2,
                'payee_name': subtransaction['payee_name']
            })

        params = {
            'transaction': {
                'account_id': self.default_account_id,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'amount': amount,
                'payee_name': their_name,
                'cleared': 'uncleared',
                'approved': False,
                'flag_color': 'blue',
                'subtransactions': subtransactions
            }
        }
        self.ynab.create_transaction(params)

    def _get_default_account_id(self):
        accounts = self.ynab.get_accounts()
        default_account_name = SECRETS[self.secrets_id]['default_account_name']
        default_accounts = list(filter(lambda i: i['name'] == default_account_name, accounts))
        assert len(default_accounts) > 0, f'No account matches {self.name} > {default_account_name}'
        assert len(default_accounts) < 2, f'Multiple accounts match {self.name} > {default_account_name}'
        return default_accounts[0]['id']
