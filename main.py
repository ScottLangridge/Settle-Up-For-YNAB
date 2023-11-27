from datetime import datetime

from Ynab import Ynab
from secrets import SECRETS

def build_settle_up_transaction_params(my_account_id, their_name, my_subtransactions, their_subtransactions):
    super_account_id = my_account_id
    super_date = datetime.now().strftime('%Y-%m-%d')
    super_amount = 0
    super_payee_name = their_name
    super_cleared = 'uncleared'
    super_approved = False
    super_flag_color = 'blue'
    super_subtransactions = []
    for subtransaction in my_subtransactions:
        super_amount -= subtransaction['amount'] // 2
        super_subtransactions.append({
            'amount': -(subtransaction['amount'] // 2),
            'payee_name': subtransaction['payee_name']
        })
    for subtransaction in their_subtransactions:
        super_amount += subtransaction['amount'] // 2
        super_subtransactions.append({
            'amount': subtransaction['amount'] // 2,
            'payee_name': subtransaction['payee_name']
        })

    return {
        'transaction': {
            'account_id': super_account_id,
            'date': super_date,
            'amount': super_amount,
            'payee_name': super_payee_name,
            'cleared': super_cleared,
            'approved': super_approved,
            'flag_color': super_flag_color,
            'subtransactions': super_subtransactions
        }
    }


if __name__ == '__main__':
    ynab = Ynab(SECRETS['user_a']['token'])

    default_accounts = list(filter(lambda i: i['name'] == SECRETS['user_a']['default_account_name'], ynab.get_accounts()))
    assert len(default_accounts) > 0, 'No account matches user_a > default_account_name'
    assert len(default_accounts) < 2, 'Multiple accounts match user_a > default_account_name'
    default_account_id = default_accounts[0]['id']

    transactions = ynab.get_transactions()
    transactions_since_last_settled = []
    for i in transactions[::-1]:
        if i['flag_color'] == 'red':
            transactions_since_last_settled.append(i)
        elif i['flag_color'] == 'blue':
            break

    params = build_settle_up_transaction_params(default_account_id, 'Scott Langridge', transactions_since_last_settled, [])
    ynab.create_transaction(params)
