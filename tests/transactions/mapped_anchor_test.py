from unittest import mock
from time import time

from lto.binary import Binary
from lto.transactions import MappedAnchor
from lto.accounts.ed25519 import AccountFactory
from lto import crypto
from freezegun import freeze_time


class TestMappedAnchor:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)


    def test_construct_zero(self):
        transaction = MappedAnchor({})
        assert transaction.tx_fee == 25000000
        assert transaction.anchors == {}

    def test_construct_one(self):
        transaction = MappedAnchor({crypto.sha256('a'): crypto.sha256('b')})
        assert transaction.tx_fee == 35000000
        assert transaction.anchors == {crypto.sha256('a'): crypto.sha256('b')}

    def test_construct_three(self):
        anchors = {
            crypto.sha256('a'): crypto.sha256('b'),
            crypto.sha256('1'): crypto.sha256('2'),
            crypto.sha256('x'): crypto.sha256('y')
        }
        transaction = MappedAnchor(anchors)
        assert transaction.tx_fee == 55000000
        assert transaction.anchors == anchors

    @freeze_time("2021-01-14")
    def test_sign_with(self):
        transaction = MappedAnchor({crypto.sha256('a'): crypto.sha256('b')})
        assert transaction.is_signed() is False
        transaction.sign_with(self.account)
        assert transaction.is_signed() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.sender_key_type == 'ed25519'
        assert transaction.sender_public_key == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verify_signature(transaction.to_binary(), transaction.proofs[0])

    @freeze_time("2021-01-14")
    def test_to_json(self):
        expected = {
            "type": 22,
            "version": 3,
            "anchors": {'EdqM52SpXCn5c1uozuvuH5o9Tcr41kYeCWz4Ymu6ngbt': '5Ba2vn7EcuaYvrhJBtUPZu8BYGFwNKjJwG8xFYskpme4'},
            "sender": "3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2",
            "senderKeyType": "ed25519",
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 35000000,
            "timestamp": 1326499200000,
            "proofs": ['3jSCbBRVJb4W9hZGFEb3CEDptbWucEEASK1ikcm5bNyWbrrdvLvCqunVJ6pFb4Yq1gTXrdcazpfgCiCLrWNNyy6L']
        }

        transaction = MappedAnchor({crypto.sha256('a'): crypto.sha256('b')})
        transaction.timestamp = 1326499200000
        transaction.version = 3
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
        transaction = MappedAnchor({crypto.sha256('a'): crypto.sha256('b')})
        broadcasted_tx = MappedAnchor({crypto.sha256('a'): crypto.sha256('b')})
        broadcasted_tx.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'

        mc = mock_PublicNode.return_value
        mc.broadcast.return_value = broadcasted_tx

        assert mc.broadcast(transaction) == broadcasted_tx

    @freeze_time("2021-01-14")
    def test_from_data(self):
        data = {
            "type": 15,
            "version": 3,
            "id": "8M6dgn85eh3bsHrVhWng8FNaHBcHEJD4MPZ5ZzCciyon",
            "sender": "3Jq8mnhRquuXCiFUwTLZFVSzmQt3Fu6F7HQ",
            "senderKeyType": "ed25519",
            "senderPublicKey": "AJVNfYjTvDD2GWKPejHbKPLxdvwXjAnhJzo6KCv17nne",
            "fee": 35000000,
            "timestamp": 1326499200000,
            "anchors": {
                'EdqM52SpXCn5c1uozuvuH5o9Tcr41kYeCWz4Ymu6ngbt': '5Ba2vn7EcuaYvrhJBtUPZu8BYGFwNKjJwG8xFYskpme4',
            },
            "proofs": ["4aMwABCZwtXrGGKmBdHdR5VVFqG51v5dPoyfDVZ7jfgD3jqc851ME5QkToQdfSRTqQmvnB9YT4tCBPcMzi59fZye"],
            "height": 1069662
            }
        transaction = MappedAnchor.from_data(data)

        assert transaction.version == 3
        assert transaction.id == "8M6dgn85eh3bsHrVhWng8FNaHBcHEJD4MPZ5ZzCciyon"
        assert transaction.sender == "3Jq8mnhRquuXCiFUwTLZFVSzmQt3Fu6F7HQ"
        assert transaction.sender_key_type == "ed25519"
        assert transaction.sender_public_key == "AJVNfYjTvDD2GWKPejHbKPLxdvwXjAnhJzo6KCv17nne"
        assert transaction.fee == 35000000
        assert transaction.timestamp == 1326499200000

        assert len(transaction.anchors) == 1
        assert "EdqM52SpXCn5c1uozuvuH5o9Tcr41kYeCWz4Ymu6ngbt" in [k.base58() for k, v in transaction.anchors.items()]
        assert transaction.anchors[Binary.frombase58("EdqM52SpXCn5c1uozuvuH5o9Tcr41kYeCWz4Ymu6ngbt")].base58() == \
               '5Ba2vn7EcuaYvrhJBtUPZu8BYGFwNKjJwG8xFYskpme4'

        assert transaction.proofs == ["4aMwABCZwtXrGGKmBdHdR5VVFqG51v5dPoyfDVZ7jfgD3jqc851ME5QkToQdfSRTqQmvnB9YT4tCBPcMzi59fZye"]
        assert transaction.height == 1069662
