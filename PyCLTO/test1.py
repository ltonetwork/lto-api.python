from PyCLTO.Transaction import Transfer
from PyCLTO import AccountFactory


#transfer(self, recipient, amount, attachment='', txFee=0, timestamp=0):
#factory =
account = AccountFactory("T").createFromPublicKey(publicKey='AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX')
account.privateKey = '3SSiggbbRiZHydbjjwV5PvvexFmWXmV4m3PV54jTkVjCgAFWrGCnxBCkbucTfFNcjxhxnmSxScUswBMmJGyUQW2M'
#print(account.privateKey)
sender = '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du'
recipient = '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb'
amount = 1234

from PyCLTO import PublicNode
#print(publicNode.balance(address=account.address))
url = 'https://testnet.lto.network'
node = PublicNode(url)
print(PublicNode(url).balance(address=account.address))
Transfer.transfer(account, recipient, amount)