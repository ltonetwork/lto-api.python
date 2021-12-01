from unittest import mock
from time import time
from lto import Anchor
from lto.accounts.account_factory_ecdsa import AccountFactoryECDSA as AccountFactory
from lto import crypto
import pytest


class TestAnchor:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)

    def test_construct(self):
        transaction = Anchor('1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89')
        assert transaction.tx_fee == 35000000
        assert transaction.anchor == '1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89'


    def test_sign_with(self):
        transaction = Anchor('1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89')
        assert transaction.is_signed() is False
        transaction.sign_with(self.account)
        assert transaction.is_signed() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MxtfVoSRZKwShuyGTpmPgpAgy8nzZ8ZJYp'
        assert transaction.sender_public_key == 'mNxM4Q8dPYpMMcHaiSvBgnX71RCqwdcR1PCc1RgDvb7J'
        assert self.account.verify_signature(transaction.to_binary(), transaction.proofs[0])

    expected_v1 = {'anchors': ['HiorsQW6E76Cp4AD51zcKcWu644ZzzraXQL286Jjzufh7U7qJroTKt7KMMpv'],
             'fee': 35000000,
             'proofs': ['5Tj642sHkXM8xHwRSy8d5Ksm5gG1YppNb8Fsn3RkXpb3cHakddyDgjJLMFNBKdw3SdZAjU5GDuYAHqXYHJmFuPQ3'],
             'sender': '3MxtfVoSRZKwShuyGTpmPgpAgy8nzZ8ZJYp',
             'senderKeyType': 'secp256k1',
             'senderPublicKey': 'mNxM4Q8dPYpMMcHaiSvBgnX71RCqwdcR1PCc1RgDvb7J',
             'timestamp': 1610142631066,
             'type': 15,
             'version': 1}

    expected_v3 = {
            "type": 15,
            "version": 3,
            "anchors": ['HiorsQW6E76Cp4AD51zcKcWu644ZzzraXQL286Jjzufh7U7qJroTKt7KMMpv'],
            "sender": "3MxtfVoSRZKwShuyGTpmPgpAgy8nzZ8ZJYp",
            "senderKeyType": "secp256k1",
            "senderPublicKey": 'mNxM4Q8dPYpMMcHaiSvBgnX71RCqwdcR1PCc1RgDvb7J',
            "fee": 35000000,
            "timestamp": 1610142631066,
            "proofs": ['3jSCbBRVJb4W9hZGFEb3CEDptbWucEEASK1ikcm5bNyWbrrdvLvCqunVJ6pFb4Yq1gTXrdcazpfgCiCLrWNNyy6L']
        }

    @pytest.mark.parametrize("version, expected", [(1, expected_v1), (3, expected_v3)])
    def test_to_json(self, expected, version):
        transaction = Anchor('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        transaction.timestamp = 1610142631066
        transaction.version = version
        transaction.sign_with(self.account)
        assert transaction.to_json() == expected

    @mock.patch('src.lto.PublicNode')
    def test_broadcast(self, mock_Class):
        transaction = Anchor('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        broadcastedTransaction = Anchor('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction
        assert mc.broadcast(transaction) == broadcastedTransaction

    def test_from_data(self):
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
        crypto.compare_data_transaction(data, transaction)