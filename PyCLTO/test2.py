from PyCLTO import AccountFactory
from PyCLTO.Transactions import Transfer
from PyCLTO import PublicNode
import base58

factory = AccountFactory("T")
sender = factory.createFromSeed(
    "cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy")
recipient = factory.createFromSeed(
    "north sibling rural deal find august paddle violin glow crucial inject goat habit toddler biology")
test = base58.b58encode(recipient.publicKey.__bytes__())
print('test', test)
#third = factory.createFromPublicKey(recipient.publicKey)
third = factory.createFromPublicKey(test)

print(third.publicKey)
print(recipient.publicKey)
print(type(third.publicKey))
print(type(recipient.publicKey))

