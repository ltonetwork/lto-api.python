from LTO.Transactions.Anchor import Anchor
from LTO.Accounts.AccountFactoryECDSA import AccountECDSA
from LTO.Accounts.AccountFactoryED25519 import AccountED25519
from LTO.PublicNode import PublicNode

seed = 'cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy'

account = AccountECDSA('T').createFromSeed(seed)
print(account.address)
#account = AccountED25519('T').createFromSeed(seed)
node = PublicNode('https://testnet.lto.network')
anchor = '6cb1bbacd93e18ec5ec5d4f5e3f5c5ba23d79e433545e8b349d5ccf67e105bd2'

transaction = Anchor(anchor)
transaction.signWith(account)
transaction.broadcastTo(node)
