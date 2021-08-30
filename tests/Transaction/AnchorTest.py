from PyCLTO.AccountFactory import AccountFactory
from PyCLTO.Transactions.Anchor import Anchor
import copy
from unittest import mock

class TestAnchor:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)

    def testContruct(self):
        transaction = Anchor('1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89')
        assert transaction.txFee == 35000000
        assert transaction.anchor == '1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89'


    def testSignWith(self):
        transaction = Anchor('1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89')
        transaction.timestamp = 1629883934685
        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])

    def dataProvider(self):
        return ({
            "type": 15,
            "version": 1,
            "anchors": 'HiorsQW6E76Cp4AD51zcKcWu644ZzzraXQL286Jjzufh7U7qJroTKt7KMMpv',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 35000000,
            "timestamp": 1610142631066,
            "proofs": ['2DAh6j1CMBTDqMTh2Y485oKV53dTjtUvCJNc7Z3r8jVJ8kBXf34YpfbZXiKSaupq7azMtu7y4GMosRGqPCYnvxcg']
        })


    def testToJson(self):
        transaction = Anchor('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        transaction.timestamp = 1610142631066
        transaction.signWith(self.account)
        assert transaction.toJson() == self.dataProvider()
        '''ret = self.dataProvider()
        tran = transaction.toJson()
        assert tran['type'] == ret['type']
        assert tran['version'] == ret['version']
        assert tran['senderPublicKey'] == ret['senderPublicKey']
        assert tran['anchors'] == ret['anchors']
        assert tran['fee'] == ret['fee']
        assert tran['timestamp'] == ret['timestamp']
        assert tran['proofs'] == ret['proofs']'''
