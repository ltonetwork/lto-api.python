from PyCLTO.AccountFactory import AccountFactory
from PyCLTO.Account import Account
import base58

factory = AccountFactory('T')
account = factory.create()

senderPubKey = account.getPublicKey()

print(bytes(account.publicKey))
'''print(type(account.publicKey.__bytes__()))
print(type(bytes(account.publicKey)))
print(senderPubKey)
print(type(base58.b58decode(senderPubKey)))'''