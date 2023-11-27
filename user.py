from secrets import SECRETS
from ynab import Ynab
from datetime import datetime


class User:
    def __init__(self, secrets_id):
        self.secrets_id = secrets_id
        self.name = SECRETS[secrets_id]['name']
        self.ynab = Ynab(SECRETS[secrets_id]['token'])
        self.default_account_id = self._get_default_account_id()
        self.split_transaction_flag = SECRETS[secrets_id]['split_transaction_flag']
        self.settle_up_transaction_flag = SECRETS[secrets_id]['settle_up_transaction_flag']

    def get_transactions_since_last_settled(self):
        last_settled_date = "1970-01-01"
        transactions = self.ynab.get_transactions()
        transactions_since_last_settled = []
        for i in transactions[::-1]:
            if i['date'] < last_settled_date:
                break
            elif i['flag_color'] == self.split_transaction_flag:
                transactions_since_last_settled.append(i)
            elif i['flag_color'] == self.settle_up_transaction_flag:
                last_settled_date = i['date']

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
                'flag_color': self.settle_up_transaction_flag,
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
