from PyCLTO.AccountFactory import AccountFactory
from PyCLTO.Transactions.Anchor import Anchor
import base58
from PyCLTO import crypto
from PyCLTO.PublicNode import PublicNode

ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
# seed2 = 'cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy'
account = AccountFactory('L').createFromSeed(ACCOUNT_SEED)
transaction = Anchor('1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89')
transaction.timestamp = 1609773456000
transaction.signWith(account)
#PublicNode('https://testnet.lto.network').broadcast(transaction)
print(transaction.proofs)

def dataProvider():
    return ({
        "type": 4,
        "version": 2,
        "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
        "recipient": '3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh',
        "amount": 120000000,
        "fee": 100000000,
        "timestamp": 1609773456000,
        "attachment": '9Ajdvzr',
        "proofs": ['PTEgvxqiUswaKiHoamMpTDRDS6u9msGoS2Hz56c16xSTHRfMnNPgbGBrDtonCspE9RErdsei7RQaFBbPWZgTJbj']
    })

json = transaction.toJson()
print(transaction.anchor)

data = dataProvider()
print(data['proofs'][0])
print(transaction.proofs[0])
print(data['proofs'] == transaction.proofs)
print(data)
print(json)
print(json == data)

print(base58.b58encode(crypto.str2bytes('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')))