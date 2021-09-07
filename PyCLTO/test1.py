from AccountFactory import AccountFactory
from PublicNode import PublicNode
from Transactions.Association import Association
from Transactions.CancelLease import CancelLease
from Transactions.Sponsor import Sponsor
from Transactions.CancelSponsor import CancelSponsor

ACCOUNT2_SEED = 'cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy'
account = AccountFactory('T').createFromSeed(ACCOUNT2_SEED)

#transaction = Association(recipient='3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du', associationType=1)

#transaction = Sponsor('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')
transaction = CancelSponsor('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')
transaction.signWith(account)

returnValue = transaction.broadcastTo(PublicNode('https://testnet.lto.network'))


