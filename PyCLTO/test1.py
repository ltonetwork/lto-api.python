import PyCLTO

ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
ACCOUNT2_SEED = 'cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy'

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

pyclto = PyCLTO.PyCLTO()
pyclto.transaction(data)

print(ret)
