from AccountFactory import AccountFactory
from Transactions.Transfer import Transfer
from PyCLTO.PublicNode import PublicNode
import crypto
ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
ACCOUNT2_SEED = 'cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy'

account = AccountFactory('T').createFromSeed(ACCOUNT2_SEED)

transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 705000000)
transaction.signWith(account)
node = PublicNode('https://testnet.lto.network')
transaction.broadcastTo(node)

crypto.validateAddress('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1')


#To check

# Lease
# Transfer

