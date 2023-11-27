from user import User

if __name__ == '__main__':
    print('creating user')
    user_a = User('user_a')

    print('fetching transactions')
    transactions_a = user_a.get_transactions_since_last_settled()

    print('creating transaction')
    user_a.create_settle_up_transaction("User B Name", transactions_a, [])

    print('done')
