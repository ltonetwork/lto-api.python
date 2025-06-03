from unittest import mock
from time import time
from lto.transactions.register import Register
from lto.accounts.ed25519 import AccountFactory
from lto import crypto
from freezegun import freeze_time


class TestRegister:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)
    account2 = AccountFactory('T').create_from_seed('tree ship container raccoon cup water mother')
    account3 = AccountFactory('T').create_from_seed('milk animal bottle raccoon yellow green')

    def test_construct(self):
        transaction = Register(self.account2, self.account3)
        assert transaction.tx_fee == 45000000
        assert type(transaction.accounts == dict)

    @freeze_time("2021-01-14")
    def test_sign_with(self):
        transaction = Register(self.account2, self.account3)
        assert transaction.is_signed() is False
        transaction.sign_with(self.account)
        assert transaction.is_signed() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.sender_key_type == 'ed25519'
        assert transaction.sender_public_key == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verify_signature(transaction.to_binary(), transaction.proofs[0])

    expected_v3 = {
            "type": 24,
            "version": 3,
            "accounts": [{'keyType': 'ed25519', 'publicKey': '8VNd1qLRyRSNdqfkjDffpFkdeUrPCGEL3btzkcr98ykX'},
             {'keyType': 'ed25519', 'publicKey': '7YVCTAzyAjrtRw5RsxjfonCn3tUrfgtYcy5xd2niqWDa'}],
            "sender": "3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2",
            "senderKeyType": "ed25519",
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 45000000,
            "timestamp": 1326499200000,
            "proofs": ['2omugkAQdrm9P7YPx6WZbXMBTifRS6ptaTT8rPRRvKFr1EPFafHSosq6HzkuuLv78gR6vaXLA9WtMsTSBgi3H1qe']
        }

    @freeze_time("2021-01-14")
    def test_to_json(self):
        transaction = Register(self.account2, self.account3)
        transaction.timestamp = 1326499200000
        transaction.sign_with(self.account)
        assert transaction.to_json() == self.expected_v3

    @mock.patch('src.lto.PublicNode')
    def test_broadcast(self, mock_PublicNode):
        transaction = Register(self.account2, self.account3)
        broadcasted_tx = Register('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        broadcasted_tx.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_PublicNode.return_value
        mc.broadcast.return_value = broadcasted_tx
        assert mc.broadcast(transaction) == broadcasted_tx

    @freeze_time("2021-01-14")
    def test_from_data(self):
        data = {
            "type": 20,
            "version": 3,
            "id": "8M6dgn85eh3bsHrVhWng8FNaHBcHEJD4MPZ5ZzCciyon",
            "sender": "3Jq8mnhRquuXCiFUwTLZFVSzmQt3Fu6F7HQ",
            "senderKeyType": "ed25519",
            "senderPublicKey": "AJVNfYjTvDD2GWKPejHbKPLxdvwXjAnhJzo6KCv17nne",
            "fee": 45000000,
            "timestamp": 1326499200000,
            "accounts": [{'keyType': 'ed25519', 'publicKey': '8VNd1qLRyRSNdqfkjDffpFkdeUrPCGEL3btzkcr98ykX'},
                         {'keyType': 'ed25519', 'publicKey': '7YVCTAzyAjrtRw5RsxjfonCn3tUrfgtYcy5xd2niqWDa'}],
            "proofs": ["2omugkAQdrm9P7YPx6WZbXMBTifRS6ptaTT8rPRRvKFr1EPFafHSosq6HzkuuLv78gR6vaXLA9WtMsTSBgi3H1qe"],
            "height": 1069662
            }
        transaction = Register.from_data(data)
        crypto.compare_data_transaction(data, transaction)
