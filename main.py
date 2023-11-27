from user import User

if __name__ == '__main__':
    print('creating user')
    user_a = User('user_a')
    user_b = User('user_b')

    print('fetching transactions')
    transactions_a = user_a.get_transactions_since_last_settled()
    transactions_b = user_b.get_transactions_since_last_settled()

    print('creating transaction')
    user_a.create_settle_up_transaction(user_b.name, transactions_a, transactions_b)
    user_a.create_settle_up_transaction(user_a.name, transactions_b, transactions_a)

    print('done')
