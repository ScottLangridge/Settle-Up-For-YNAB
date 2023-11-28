# Settle-Up-For-YNAB
## Goal
Allow two YNAB users who frequently split costs to create settle up transactions with one button.

Settle up transactions work as described by [Splitwise and YNAB: A Guide > Splitwise in Your Register](https://support.ynab.com/en_us/splitwise-and-ynab-a-guide-H1GwOyuCq#register), except that instead of splitwise, transactions made by the other person are sourced from their YNAB.

## Usage
Tag transactions which should be split with a flag. When the code is run, all newly tagged transactions since the last split will be fetched and they will be combined into a matching settle up transaction on each users budget.

## Setup
1. `pip install -r requirements.txt`
1. `cp secrets.template.py secrets.py`
1. [Create a personal access token for each user](https://app.ynab.com/settings/developer) (OAuth currenlty unsupported)
1. Update `secrets.py` according to the Secrets section below.

## Secrets
- `user_a/b`: These are just unique identifiers for the two users and can be left alone.
- `token`: The personal access token generated prior.
- `name`: The name that should appear for that user in the payee section of settle up transactions.
- `default_account_name`: The name of the account that new settle up transactions should go to by default.
- `split_transaction_flag`: The colour of flag that the user will use to define transactions which should be split (`red`, `orange`, `yellow`, `green`, `blue`, `purple
- `settle_up_transaction_flag`: The colour of flag that the user will use to define settle up transactions (`red`, `orange`, `yellow`, `green`, `blue`, `purple`).
