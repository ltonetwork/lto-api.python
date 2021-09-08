from AccountFactory import AccountFactory
from PublicNode import PublicNode
from Transactions.Association import Association
from Transactions.RevokeAssociation import RevokeAssociation
from Transactions.CancelLease import CancelLease
from Transactions.Sponsor import Sponsor

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
from Transactions.Sponsor import Sponsor
from Transactions.CancelSponsor import CancelSponsor

ACCOUNT2_SEED = 'cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy'
account = AccountFactory('T').createFromSeed(ACCOUNT2_SEED)
node = PublicNode('https://testnet.lto.network')

#transaction = Association(recipient='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', anchor='4yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
#transaction2 = RevokeAssociation(recipient='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', associationType=1, anchor='9yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
#transaction = Sponsor('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')
#transaction = CancelSponsor('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')

#transfer = CancelLease(leaseId='GZmfQ8C2L1ynoetqTkZ3brX6XAxLp2jad5gC2bkT21DG')
#transfer = Sponsor(recipient='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')
transfer = CancelSponsor(recipient='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')


transfer.signWith(account)
returnValue = transfer.broadcastTo(node)


