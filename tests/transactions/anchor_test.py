from unittest import mock
from time import time

from lto.binary import Binary
from lto.transactions import Anchor
from lto.accounts.ed25519 import AccountFactory
from lto import crypto
import pytest
from freezegun import freeze_time


class TestAnchor:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)


    def test_construct_zero(self):
        transaction = Anchor()
        assert transaction.tx_fee == 25000000
        assert transaction.anchors == []

    def test_construct_one(self):
        transaction = Anchor(crypto.sha256('a'))
        assert transaction.tx_fee == 35000000
        assert transaction.anchors == [crypto.sha256('a')]

    def test_construct_three(self):
        transaction = Anchor(crypto.sha256('a'), crypto.sha256('b'), crypto.sha256('c'))
        assert transaction.tx_fee == 55000000
        assert transaction.anchors == [crypto.sha256('a'), crypto.sha256('b'), crypto.sha256('c')]

    @freeze_time("2021-01-14")
    def test_sign_with(self):
        transaction = Anchor(crypto.sha256(''))
        assert transaction.is_signed() is False
        transaction.sign_with(self.account)
        assert transaction.is_signed() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.sender_key_type == 'ed25519'
        assert transaction.sender_public_key == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verify_signature(transaction.to_binary(), transaction.proofs[0])

    expected_v1 = {
             'anchors': ['GKot5hBsd81kMupNCXHaqbhv3huEbxAFMLnpcX2hniwn'],
             'fee': 35000000,
             'proofs': ['5Tj642sHkXM8xHwRSy8d5Ksm5gG1YppNb8Fsn3RkXpb3cHakddyDgjJLMFNBKdw3SdZAjU5GDuYAHqXYHJmFuPQ3'],
             'sender': '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
             'senderKeyType': 'ed25519',
             'senderPublicKey': '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
             'timestamp': 1326499200000,
             'type': 15,
             'version': 1}

    expected_v3 = {
            "type": 15,
            "version": 3,
            "anchors": ['GKot5hBsd81kMupNCXHaqbhv3huEbxAFMLnpcX2hniwn'],
            "sender": "3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2",
            "senderKeyType": "ed25519",
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 35000000,
            "timestamp": 1326499200000,
            "proofs": ['3jSCbBRVJb4W9hZGFEb3CEDptbWucEEASK1ikcm5bNyWbrrdvLvCqunVJ6pFb4Yq1gTXrdcazpfgCiCLrWNNyy6L']
        }

    @freeze_time("2021-01-14")
    @pytest.mark.parametrize("version, expected", [(1, expected_v1), (3, expected_v3)])
    def test_to_json(self, version, expected):
        transaction = Anchor(crypto.sha256(''))
        transaction.timestamp = 1326499200000
        transaction.version = version
        transaction.sign_with(self.account)

        actual = transaction.to_json()
        assert actual['type'] == expected['type']
        assert actual['version'] == expected['version']
        assert actual['anchors'] == expected['anchors']
        assert actual['sender'] == expected['sender']
        assert actual['senderKeyType'] == expected['senderKeyType']
        assert actual['senderPublicKey'] == expected['senderPublicKey']
        assert actual['fee'] == expected['fee']
        assert actual['timestamp'] == expected['timestamp']

    @mock.patch('src.lto.PublicNode')
    def test_broadcast(self, mock_PublicNode):
        transaction = Anchor(Binary.frombase58('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk'))
        broadcasted_tx = Anchor(Binary.frombase58('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk'))
        broadcasted_tx.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'

        mc = mock_PublicNode.return_value
        mc.broadcast.return_value = broadcasted_tx

        assert mc.broadcast(transaction) == broadcasted_tx

    @freeze_time("2021-01-14")
    def test_from_data(self):
        data = {
            "type": 15,
            "version": 1,
            "id": "8M6dgn85eh3bsHrVhWng8FNaHBcHEJD4MPZ5ZzCciyon",
            "sender": "3Jq8mnhRquuXCiFUwTLZFVSzmQt3Fu6F7HQ",
            "senderKeyType": "ed25519",
            "senderPublicKey": "AJVNfYjTvDD2GWKPejHbKPLxdvwXjAnhJzo6KCv17nne",
            "fee": 35000000,
            "timestamp": 1326499200000,
            "anchors": ["5SbkwAekNbaG8P1mTDdAE88mpWtCdET9vTmV2v9vQsCK", "3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk"],
            "proofs": ["4aMwABCZwtXrGGKmBdHdR5VVFqG51v5dPoyfDVZ7jfgD3jqc851ME5QkToQdfSRTqQmvnB9YT4tCBPcMzi59fZye"],
            "height": 1069662
            }
        transaction = Anchor.from_data(data)

        assert transaction.version == 1
        assert transaction.id == "8M6dgn85eh3bsHrVhWng8FNaHBcHEJD4MPZ5ZzCciyon"
        assert transaction.sender == "3Jq8mnhRquuXCiFUwTLZFVSzmQt3Fu6F7HQ"
        assert transaction.sender_key_type == "ed25519"
        assert transaction.sender_public_key == "AJVNfYjTvDD2GWKPejHbKPLxdvwXjAnhJzo6KCv17nne"
        assert transaction.fee == 35000000
        assert transaction.timestamp == 1326499200000

        assert len(transaction.anchors) == 2
        assert type(transaction.anchors[0]) == Binary
        assert transaction.anchors[0].base58() == "5SbkwAekNbaG8P1mTDdAE88mpWtCdET9vTmV2v9vQsCK"
        assert transaction.anchors[1].base58() == "3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk"

        assert transaction.proofs == ["4aMwABCZwtXrGGKmBdHdR5VVFqG51v5dPoyfDVZ7jfgD3jqc851ME5QkToQdfSRTqQmvnB9YT4tCBPcMzi59fZye"]
        assert transaction.height == 1069662
