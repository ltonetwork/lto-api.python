from unittest import mock
from time import time
from LTO import Anchor
from LTO.Accounts.AccountFactoryECDSA import AccountECDSA as AccountFactory


class TestAnchor:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)

    def testContruct(self):
        transaction = Anchor('1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89')
        assert transaction.txFee == 35000000
        assert transaction.anchor == '1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89'


    def testSignWith(self):
        transaction = Anchor('1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89')
        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MxtfVoSRZKwShuyGTpmPgpAgy8nzZ8ZJYp'
        assert transaction.senderPublicKey == 'mNxM4Q8dPYpMMcHaiSvBgnX71RCqwdcR1PCc1RgDvb7J'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])

    def expectedV1(self):
        return ({
            "type": 15,
            "version": 1,
            "anchors": ['HiorsQW6E76Cp4AD51zcKcWu644ZzzraXQL286Jjzufh7U7qJroTKt7KMMpv'],
            'sender': '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 35000000,
            "timestamp": 1610142631066,
            "proofs": ['2DAh6j1CMBTDqMTh2Y485oKV53dTjtUvCJNc7Z3r8jVJ8kBXf34YpfbZXiKSaupq7azMtu7y4GMosRGqPCYnvxcg']
        })

    def expectedV3(self):
        return ({
            "type": 15,
            "version": 3,
            "anchors": ['HiorsQW6E76Cp4AD51zcKcWu644ZzzraXQL286Jjzufh7U7qJroTKt7KMMpv'],
            "sender": "3MxtfVoSRZKwShuyGTpmPgpAgy8nzZ8ZJYp",
            "senderKeyType": "secp256k1",
            "senderPublicKey": 'mNxM4Q8dPYpMMcHaiSvBgnX71RCqwdcR1PCc1RgDvb7J',
            "fee": 35000000,
            "timestamp": 1610142631066,
            "proofs": ['3jSCbBRVJb4W9hZGFEb3CEDptbWucEEASK1ikcm5bNyWbrrdvLvCqunVJ6pFb4Yq1gTXrdcazpfgCiCLrWNNyy6L']
        })

    def testToJson(self):
        transaction = Anchor('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        transaction.timestamp = 1610142631066
        transaction.signWith(self.account)
        if transaction.version == 1:
            expected = self.expectedV1()
        elif transaction.version == 3:
            expected = self.expectedV3()
        else:
            expected = ''

        assert transaction.toJson() == expected

    @mock.patch('src.LTO.PublicNode')
    def testBroadcast(self, mock_Class):
        transaction = Anchor('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        broadcastedTransaction = Anchor('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction
        assert mc.broadcast(transaction) == broadcastedTransaction

    def testFromData(self):
        data = {
            "type": 15,
            "version": 1,
            "id": "8M6dgn85eh3bsHrVhWng8FNaHBcHEJD4MPZ5ZzCciyon",
            "sender": "3Jq8mnhRquuXCiFUwTLZFVSzmQt3Fu6F7HQ",
            "senderKeyType": "ed25519",
            "senderPublicKey": "AJVNfYjTvDD2GWKPejHbKPLxdvwXjAnhJzo6KCv17nne",
            "fee": 35000000,
            "timestamp": 1610397549043,
            "anchors": ["5SbkwAekNbaG8P1mTDdAE88mpWtCdET9vTmV2v9vQsCK"],
            "proofs": ["4aMwABCZwtXrGGKmBdHdR5VVFqG51v5dPoyfDVZ7jfgD3jqc851ME5QkToQdfSRTqQmvnB9YT4tCBPcMzi59fZye"],
            "height": 1069662
            }
        transaction = Anchor(anchor='').fromData(data)
        for key in data:
            assert data[key] == transaction.__getattr__(key)