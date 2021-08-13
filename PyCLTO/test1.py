from PyCLTO.Transactions import Transfer
from PyCLTO import AccountFactory
from PyCLTO import Account as acc


factory = AccountFactory("T")
account = factory.createFromPublicKey(publicKey='AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX')
account.privateKey = '3SSiggbbRiZHydbjjwV5PvvexFmWXmV4m3PV54jTkVjCgAFWrGCnxBCkbucTfFNcjxhxnmSxScUswBMmJGyUQW2M'
recipient = factory.createFromPublicKey("7DoUKkFDUX5Njhh7ZgiZx2gi5PuAHhXWgWSj27CH97x")
recipient.privateKey = "2jtHeu4GgXf7VHZzGzuFXwgKsGYGxUrypPGZQY84Nvs358EvfWPf3psuwkGoxCjX2zbA9FwsBiXhbT26wmjubW9p"
amount = 1234

transfer = Transfer(recipient, amount, attachment='', txFee=0, timestamp=0)
transfer.signWith(account)
'''

from PyCLTO import PublicNode
#print(publicNode.balance(address=account.address))
url = 'https://testnet.lto.network'
node = PublicNode(url)
print(PublicNode(url).balance(address=account.address))

node.broadcast(transfer)

from crypto import sign
print(sign(account.privateKey, message='test') )'''