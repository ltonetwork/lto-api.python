from AccountFactory import AccountFactory
from PublicNode import PublicNode
from Transactions.Association import Association
from Transactions.RevokeAssociation import RevokeAssociation
from Transactions.Transfer import Transfer

from Transactions.CancelLease import CancelLease
from Transactions.Sponsor import Sponsor
from Transactions.CancelSponsor import CancelSponsor

ACCOUNT2_SEED = 'cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy'
account = AccountFactory('T').createFromSeed(ACCOUNT2_SEED)

#transaction = Association(recipient='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', anchor='4yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
#transaction2 = RevokeAssociation(recipient='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', associationType=1, anchor='9yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
#transaction = Sponsor('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')
#transaction = CancelSponsor('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')
transfer = Transfer(recipient='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', amount=100000000)
transfer.signWith(account)
returnValue = transfer.broadcastTo(PublicNode('https://testnet.lto.network'))


