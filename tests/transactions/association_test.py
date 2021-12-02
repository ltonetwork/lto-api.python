from lto.accounts.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from lto.transactions.association import Association
from unittest import mock
from time import time
from lto import crypto
import pytest
from freezegun import freeze_time


class TestAssociation:
    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)

    def test_construct(self):
        transaction = Association('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1)
        assert transaction.tx_fee == 100000000
        assert transaction.association_type == 1
        assert transaction.recipient == '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1'

    @freeze_time("2021-01-14")
    def test_sign_with(self):
        transaction = Association('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1)
        assert transaction.is_signed() is False
        transaction.sign_with(self.account)
        assert transaction.is_signed() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.sender_public_key == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verify_signature(transaction.to_binary(), transaction.proofs[0])

    expected_v1 = {
        'associationType': 1,
        'fee': 100000000,
        'senderKeyType': 'ed25519',
        'hash': 'HiorsQW6E76Cp4AD51zcKcWu644ZzzraXQL286Jjzufh7U7qJroTKt7KMMpv',
        'proofs': ['3pX89U3uEYV2MA5gJWDsXRWC8Wnynd9T4X6LraQr7eNL1KmcgBiMxaT4adKqsYZMFxGTc5mpNao9WTziNTndLLEQ'],
        'recipient': '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
        'sender': '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
        'senderPublicKey': '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
        'timestamp': 1629883934685,
        'type': 16,
        'version': 1}

    expected_v3 = {
        "type": 16,
        "version": 3,
        "sender": "3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2",
        "senderKeyType": "ed25519",
        "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
        "recipient": '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
        "associationType": 1,
        "hash": 'HiorsQW6E76Cp4AD51zcKcWu644ZzzraXQL286Jjzufh7U7qJroTKt7KMMpv',
        "timestamp": 1629883934685,
        "expires": 1926499200000,
        "fee": 100000000,
        "proofs": ['3SrqBPd4XgwkFkqZpP7rDCwgV7iVxCJBpNCFv61E3ChsZ1msVPLYe3Rus1vWPCehgiDVK8579CF9ARxpVWYDSPja'],
    }

    @freeze_time("2021-01-14")
    @pytest.mark.parametrize("version, expected", [(1, expected_v1), (3, expected_v3)])
    def test_to_json(self, expected, version):
        transaction = Association('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1,
                                  anchor='3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk', expires=1926499200000)
        transaction.timestamp = 1629883934685
        transaction.version = version
        transaction.sign_with(self.account)
        assert transaction.to_json() == expected

    @mock.patch('src.lto.PublicNode')
    def test_broadcast(self, mock_Class):
        transaction = Association('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1,
                                  anchor='3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        broadcastedTransaction = Association('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1,
                                             anchor='3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction
        assert mc.broadcast(transaction) == broadcastedTransaction

    @freeze_time("2021-01-14")
    def test_from_data(self):
        data = {
            "type": 16,
            "version": 3,
            "recipient": "3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh",
            "associationType": 1,
            "hash": "3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj",
            "id": "1uZqDjRjaehEceSxrVxz6WD6wt8su8TBHyDLQ1KFnJo",
            "sender": "3NBcx7AQqDopBj3WfwCVARNYuZyt1L9xEVM",
            "senderPublicKey": "7gghhSwKRvshZwwh6sG97mzo1qoFtHEQK7iM4vGcnEt7",
            "timestamp": 1610404930000,
            "expires": 1926499200000,
            "fee": 100000000,
            "proofs": [
                "2jQMruoLoshfKe6FAUbA9vmVVvAt8bVpCFyM75Z2PLJiuRmjmLzFpM2UmgQ6E73qn46AVQprQJPBhQe92S7iSXbZ"
            ],
            "height": 1225712
        }
        transaction = Association(recipient='', association_type='').from_data(data)

        crypto.compare_data_transaction(data, transaction)
