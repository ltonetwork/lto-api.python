from unittest import mock
from time import time
from lto import Anchor
from lto.accounts.account_factory_ecdsa import AccountFactoryECDSA as AccountFactory


class TestAnchor:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)

    def testContruct(self):
        transaction = Anchor('1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89')
        assert transaction.tx_fee == 35000000
        assert transaction.anchor == '1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89'


    def testsign_with(self):
        transaction = Anchor('1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89')
        assert transaction.is_signed() is False
        transaction.sign_with(self.account)
        assert transaction.is_signed() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MxtfVoSRZKwShuyGTpmPgpAgy8nzZ8ZJYp'
        assert transaction.sender_public_key == 'mNxM4Q8dPYpMMcHaiSvBgnX71RCqwdcR1PCc1RgDvb7J'
        assert self.account.verify_signature(transaction.to_binary(), transaction.proofs[0])

    def expectedV1(self):
        return ({
            "type": 15,
            "version": 1,
            "anchors": ['HiorsQW6E76Cp4AD51zcKcWu644ZzzraXQL286Jjzufh7U7qJroTKt7KMMpv'],
            'sender': '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "public_keyKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
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
            "public_keyKey": 'mNxM4Q8dPYpMMcHaiSvBgnX71RCqwdcR1PCc1RgDvb7J',
            "fee": 35000000,
            "timestamp": 1610142631066,
            "proofs": ['3jSCbBRVJb4W9hZGFEb3CEDptbWucEEASK1ikcm5bNyWbrrdvLvCqunVJ6pFb4Yq1gTXrdcazpfgCiCLrWNNyy6L']
        })

    def testto_json(self):
        transaction = Anchor('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        transaction.timestamp = 1610142631066
        transaction.sign_with(self.account)
        if transaction.version == 1:
            expected = self.expectedV1()
        elif transaction.version == 3:
            expected = self.expectedV3()
        else:
            expected = ''

        assert transaction.to_json() == expected

    @mock.patch('src.lto.PublicNode')
    def testBroadcast(self, mock_Class):
        transaction = Anchor('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        broadcastedTransaction = Anchor('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction
        assert mc.broadcast(transaction) == broadcastedTransaction

    def testfrom_data(self):
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
        transaction = Anchor(anchor='').from_data(data)
        for key in data:
            assert data[key] == transaction.__getattr__(key)