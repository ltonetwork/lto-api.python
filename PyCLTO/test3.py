from PyCLTO import AccountFactory
from PyCLTO.Transactions import Transfer
from PyCLTO import PublicNode

factory = AccountFactory("T")
sender = factory.createFromSeed(
    "cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy")
recipient = factory.createFromSeed(
    "north sibling rural deal find august paddle violin glow crucial inject goat habit toddler biology")

transfer = Transfer.Transfer(recipient, 12340000)

transfer.signWith(sender)
print(transfer.signature)



url = 'https://testnet.lto.network'
node = PublicNode(url)

node.broadcast(transfer)


