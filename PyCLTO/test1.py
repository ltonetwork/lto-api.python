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

print('this', (19).to_bytes(1, 'big'))
print(bytes(19))
print(b'\x13')

ACCOUNT2_SEED = 'cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy'
account = AccountFactory('T').createFromSeed(ACCOUNT2_SEED)
#node = PublicNode('https://testnet.lto.network')
node = PublicNode('http://116.203.167.231:6869')

#transaction = Association(recipient='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', anchor='4yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
#transaction2 = RevokeAssociation(recipient='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', associationType=1, anchor='9yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
#transaction = CancelSponsorship('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')

transfer = Sponsorship('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')
#transfer = CancelSponsorship(recipient='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')
transfer.signWith(account)
#returnValue = transfer.broadcastTo(node)

if False and False:
    print('si')
else:
    print('no')
