from AccountFactory import AccountFactory
from Transactions.Transfer import Transfer
from PyCLTO.PublicNode import PublicNode
import crypto
from PyCLTO.Transaction import Transaction

ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
ACCOUNT2_SEED = 'cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy'

account = AccountFactory('T').createFromSeed(ACCOUNT2_SEED)

transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 705000000)
transaction.signWith(account)
node = PublicNode('https://testnet.lto.network')
transaction.broadcastTo(node)

data = {
            "type": 4,
            "version": 2,
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "recipient": '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb',
            "amount": 120000000,
            "fee": 100000000,
            "timestamp": 1609773456000,
            "attachment": '9Ajdvzr',
            "proofs": ['QJXntVh9422tFcFgzM6edXdVGdcvd9GU35S6FGQSRZKwSqG6PYmf9dsHwdXgKqdDX6m3NrxKQQcCy4yjMZHhaAS']
        }

print(Transaction().fromData(data))

#crypto.validateAddress('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1')



