from PyCLTO import AccountFactory
from PyCLTO.Transactions import Transfer
from PyCLTO import PublicNode
import base58

factory = AccountFactory("T")
sender = factory.createFromSeed(
    "cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy")
recipient = factory.createFromSeed(
    "north sibling rural deal find august paddle violin glow crucial inject goat habit toddler biology")

transfer = Transfer.Transfer(recipient.address, 12350000)


transfer.signWith(sender)



url = 'https://testnet.lto.network'
node = PublicNode(url)

node.broadcast(transfer)



sender2 = factory.createFromPublicKey('AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX')
print(base58.b58decode(sender2.publicKey))
print(sender2.privateKey)
print(sender2.address)