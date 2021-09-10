from AccountFactory import AccountFactory
from PublicNode import PublicNode
from Transactions.Association import Association
from Transactions.RevokeAssociation import RevokeAssociation
from Transactions.CancelLease import CancelLease
from Transactions.Sponsorship import Sponsorship
from Transactions.Transfer import Transfer

from Transactions.Anchor import Anchor
# Transfer = ok
# Anchor   = ok
# Association = ok
# Revoke Ass = ok
# Lease    = ok
# Cancel Lease = not ok
# Sponsor   = ok
# Cancel Sponsor = not ok


from Transactions.CancelLease import CancelLease
from Transactions.Sponsorship import Sponsorship
from Transactions.CancelSponsorship import CancelSponsorship
from Transactions.MassTransferLto import MassTransferLTO



ACCOUNT2_SEED = 'cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy'
account = AccountFactory('T').createFromSeed(ACCOUNT2_SEED)
#node = PublicNode('https://testnet.lto.network')
node = PublicNode('http://116.203.167.231:6869')

transfers = [{'recipient': '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', 'amount': 700000000}, {'recipient': '3NBC7ETcdPbf4QAXSop5UCJ53yX34aGPXoz', 'amount': 1000000}]


#transaction = Transfer('3NBC7ETcdPbf4QAXSop5UCJ53yX34aGPXoz', 100000000)
transaction = MassTransferLTO(transfers)
transaction.signWith(account)
returnValue = transaction.broadcastTo(node)
