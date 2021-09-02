import PyCLTO

ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
ACCOUNT2_SEED = 'cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy'

from Transactions.Transfer import Transfer
from AccountFactory import AccountFactory
from PublicNode import PublicNode

account = AccountFactory('T').createFromSeed(ACCOUNT2_SEED)

transaction = Transfer(amount=10000000000,recipient='3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
transaction.signWith(account)

returnValue = transaction.broadcastTo(PublicNode('https://testnet.lto.network'))

print(returnValue.id)
print(returnValue.type)
print(returnValue.proofs)