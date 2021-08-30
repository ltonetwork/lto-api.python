from AccountFactory import AccountFactory
from Transactions.Transfer import Transfer

ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
ACCOUNT2_SEED = 'cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy'

account = AccountFactory('T').createFromSeed(ACCOUNT2_SEED)
transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 705000000)
transaction.signWith(account)

