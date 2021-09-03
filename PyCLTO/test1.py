from Transactions.Transfer import Transfer
from AccountFactory import AccountFactory
from PublicNode import PublicNode
from PyCLTO import crypto
from time import time


ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
ACCOUNT2_SEED = 'cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy'



account = AccountFactory('T').createFromSeed(ACCOUNT2_SEED)

transaction = Transfer(amount=100000000,recipient='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')

transaction.signWith(account)

returnValue = transaction.broadcastTo(PublicNode('https://testnet.lto.network'))

