from secrets import SECRETS
from Ynab import Ynab

if __name__ == '__main__':
    ynab = Ynab(SECRETS['token'])
