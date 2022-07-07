from copy import deepcopy

from lto.binary import Binary
from lto.transactions.revoke_association import RevokeAssociation
from lto.accounts.ed25519.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from time import time
from unittest import mock
import pytest
from freezegun import freeze_time


class TestRevokeAssociation:
    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)

    def test_construct(self):
        transaction = RevokeAssociation('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1)
        assert transaction.recipient == '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1'
        assert transaction.association_type == 1
        assert transaction.tx_fee == 100000000

    @freeze_time("2021-01-14")
    def test_sign_with(self):
        transaction = RevokeAssociation(
            '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
            1,
            Binary.frombase58('3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
        )
        assert transaction.is_signed() is False
        transaction.sign_with(self.account)
        assert transaction.is_signed() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.subject == Binary.frombase58('3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.sender_key_type == 'ed25519'
        assert transaction.sender_public_key == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verify_signature(transaction.to_binary(), transaction.proofs[0])

    expected_v1 = {
        "type": 17,
        "version": 1,
        "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
        "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
        "subject": '3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj',
        "associationType": 1,
        "recipient": '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
        "fee": 100000000,
        'senderKeyType': 'ed25519',
        "timestamp": 1326499200000,
        "proofs": ['37xuZynPCruJpKcogFmUPXq6wyEUi3vDB18NqyHyovyVpwY1SaKNHQph2URGv4o6d72b8aEZr9p1vKCBwY9vZpFv']
    }

    expected_v3 = {
        "type": 17,
        "version": 3,
        "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
        "senderKeyType": "ed25519",
        "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
        "recipient": '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
        "associationType": 1,
        "subject": '3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj',
        "timestamp": 1326499200000,
        "fee": 100000000,
        "proofs": ['3niC7opYouRWX18SaCybwnFRqyzCJYnE3Y5rFCNWYfvDRvCZ1iSeGHxd9dDHdQKY85tgHszhV7AXNTTKHvfmgHE5']
    }

    @freeze_time("2021-01-14")
    @pytest.mark.parametrize("version, expected", [(1, expected_v1), (3, expected_v3)])
    def test_to_json(self, expected, version):
        transaction = RevokeAssociation(
            '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
            1,
            Binary.frombase58('3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
        )
        transaction.timestamp = 1326499200000
        transaction.version = version
        transaction.sign_with(self.account)
        assert transaction.to_json() == expected

    @mock.patch('src.lto.PublicNode')
    def test_broadcast(self, mock_PublicNode):
        transaction = RevokeAssociation(
            '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
            1,
            Binary.frombase58('3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
        )
        broadcasted_tx = deepcopy(transaction)
        broadcasted_tx.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'

        mc = mock_PublicNode.return_value
        mc.broadcast.return_value = broadcasted_tx

        assert mc.broadcast(transaction) == broadcasted_tx

    @freeze_time("2021-01-14")
    def test_from_data(self):
        data = {
            "type": 16,
            "version": 1,
            "recipient": "3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh",
            "associationType": 1,
            "subject": "3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj",
            "id": "1uZqDjRjaehEceSxrVxz6WD6wt8su8TBHyDLQ1KFnJo",
            "sender": "3NBcx7AQqDopBj3WfwCVARNYuZyt1L9xEVM",
            "senderPublicKey": "7gghhSwKRvshZwwh6sG97mzo1qoFtHEQK7iM4vGcnEt7",
            "timestamp": 1610404930000,
            "fee": 100000000,
            "proofs": [
                "2jQMruoLoshfKe6FAUbA9vmVVvAt8bVpCFyM75Z2PLJiuRmjmLzFpM2UmgQ6E73qn46AVQprQJPBhQe92S7iSXbZ"
            ],
            "height": 1225712
        }
        transaction = RevokeAssociation.from_data(data)

        assert transaction.version == 1
        assert transaction.id == "1uZqDjRjaehEceSxrVxz6WD6wt8su8TBHyDLQ1KFnJo"
        assert transaction.sender == "3NBcx7AQqDopBj3WfwCVARNYuZyt1L9xEVM"
        assert transaction.sender_key_type == "ed25519"
        assert transaction.sender_public_key == "7gghhSwKRvshZwwh6sG97mzo1qoFtHEQK7iM4vGcnEt7"
        assert transaction.fee == 100000000
        assert transaction.timestamp == 1610404930000

        assert transaction.association_type == 1
        assert transaction.subject.base58() == '3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj'

        assert transaction.proofs == [
            "2jQMruoLoshfKe6FAUbA9vmVVvAt8bVpCFyM75Z2PLJiuRmjmLzFpM2UmgQ6E73qn46AVQprQJPBhQe92S7iSXbZ"
        ]
        assert transaction.height == 1225712
