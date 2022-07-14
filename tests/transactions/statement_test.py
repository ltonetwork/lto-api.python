from copy import deepcopy
from lto.accounts.ed25519.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from lto.binary import Binary
from lto.transactions.data_entry import DataEntry
from lto.transactions.statement import Statement
from unittest import mock
from time import time
import pytest
from freezegun import freeze_time


class TestStatement:
    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)
    data_entries = {
        "test": 1,
        "second": True
    }

    def test_construct(self):
        transaction = Statement(1)
        assert transaction.tx_fee == 50000000
        assert transaction.statement_type == 1
        assert transaction.recipient is None
        assert transaction.subject == Binary()
        assert transaction.data == []

    def test_construct_with_data(self):
        transaction = Statement(
            statement_type=1,
            recipient='3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
            subject=bytes(b'abc'),
            data=self.data_entries
        )

        assert transaction.tx_fee == 60000000
        assert transaction.statement_type == 1
        assert transaction.recipient == '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1'
        assert transaction.subject == Binary(b'abc')
        assert (transaction.data[0].key == 'test')
        assert (transaction.data[0].type == 'integer')
        assert (transaction.data[0].value == 1)
        assert (transaction.data[1].key == 'second')
        assert (transaction.data[1].type == 'boolean')
        assert (transaction.data[1].value is True)

    @freeze_time("2021-01-14")
    def test_sign_with(self):
        transaction = Statement(1, '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', bytes(b'abc'))
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
        "type": 23,
        "version": 3,
        "fee": 60000000,
        "timestamp": 1629883934685,
        "sender": "3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2",
        "senderKeyType": "ed25519",
        "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
        "recipient": '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
        "statementType": 1,
        "subject": '3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk',
        "data": [
            {'key': 'test', 'type': 'integer', 'value': 1},
            {'key': 'second', 'type': 'boolean', 'value': True}
        ],
        "proofs": ['ZkWhjCR4fypA5UxRiAeN2YVxnj2fLCxqEr1o2YNUwULpHisiLykknxD9XEVRqrHBHox7cM56hzayejFwQAD4Q6J']
    }

    @freeze_time("2021-01-14")
    @pytest.mark.parametrize("version, expected", [(3, expected_v3)])
    def test_to_json(self, version, expected):
        transaction = Statement(recipient='3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
                                statement_type=1,
                                subject=Binary.frombase58('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk'),
                                data=self.data_entries)
        transaction.timestamp = 1629883934685
        transaction.version = version
        transaction.sign_with(self.account)
        assert transaction.to_json() == expected

    @mock.patch('src.lto.PublicNode')
    def test_broadcast(self, mock_PublicNode):
        transaction = Statement(recipient='3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
                                statement_type=1,
                                subject=Binary.frombase58('3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk'))
        broadcasted_tx = deepcopy(transaction)
        broadcasted_tx.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'

        mc = mock_PublicNode.return_value
        mc.broadcast.return_value = broadcasted_tx

        assert mc.broadcast(transaction) == broadcasted_tx

    @freeze_time("2021-01-14")
    def test_from_data(self):
        data = {
            "type": 23,
            "version": 3,
            "recipient": "3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh",
            "id": "1uZqDjRjaehEceSxrVxz6WD6wt8su8TBHyDLQ1KFnJo",
            "sender": "3NBcx7AQqDopBj3WfwCVARNYuZyt1L9xEVM",
            "senderPublicKey": "7gghhSwKRvshZwwh6sG97mzo1qoFtHEQK7iM4vGcnEt7",
            "timestamp": 1610404930000,
            "expires": 1926499200000,
            "fee": 100000000,
            "statementType": 1,
            "subject": "3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj",
            "data": [
                {'key': 'test', 'type': 'integer', 'value': 1},
                {'key': 'second', 'type': 'boolean', 'value': True}
            ],
            "proofs": [
                "2jQMruoLoshfKe6FAUbA9vmVVvAt8bVpCFyM75Z2PLJiuRmjmLzFpM2UmgQ6E73qn46AVQprQJPBhQe92S7iSXbZ"
            ],
            "height": 1225712
        }
        transaction = Statement.from_data(data)

        assert transaction.version == 3
        assert transaction.id == "1uZqDjRjaehEceSxrVxz6WD6wt8su8TBHyDLQ1KFnJo"
        assert transaction.sender == "3NBcx7AQqDopBj3WfwCVARNYuZyt1L9xEVM"
        assert transaction.sender_key_type == "ed25519"
        assert transaction.sender_public_key == "7gghhSwKRvshZwwh6sG97mzo1qoFtHEQK7iM4vGcnEt7"
        assert transaction.fee == 100000000
        assert transaction.timestamp == 1610404930000

        assert transaction.statement_type == 1
        assert transaction.subject.base58() == '3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj'

        assert len(transaction.data) == 2
        assert transaction.data[0].key == 'test'
        assert transaction.data[0].type == 'integer'
        assert transaction.data[0].value == 1
        assert transaction.data[1].key == 'second'
        assert transaction.data[1].type == 'boolean'
        assert transaction.data[1].value == True

        assert transaction.proofs == [
            "2jQMruoLoshfKe6FAUbA9vmVVvAt8bVpCFyM75Z2PLJiuRmjmLzFpM2UmgQ6E73qn46AVQprQJPBhQe92S7iSXbZ"
        ]
        assert transaction.height == 1225712
