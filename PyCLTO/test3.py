from PyCLTO import AccountFactory
from PyCLTO.Transactions import Transfer
from PyCLTO import PublicNode

factory = AccountFactory("T")
sender = factory.createFromSeed(
    "cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy")
recipient = factory.createFromSeed(
    "north sibling rural deal find august paddle violin glow crucial inject goat habit toddler biology")

transfer = Transfer.Transfer(recipient, 12340000)

print(transfer.signature)
transfer.signWith(sender)



import json
url = 'https://testnet.lto.network'
node = PublicNode(url)
transaction = transfer.toJson(sender)
print(transaction)
#node.broadcast(transaction)



x = json.dumps({'type': 4, 'version': 2, 'senderPublicKey': 'AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX', 'recipient': '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 'amount': 12340000, 'fee': 100000000, 'timestamp': 1628784385549, 'attachment': '', 'proofs': ['5z3inJyXHif4FJ2g6D2SGtHFRKjuZmd93GeeDabE1GDxSJYc7m1kyEedHp4ieXF3V5e9WoGhMan8m9mmtZthdFoX']})

test = json.dumps(transaction)
print(x)
print(test)