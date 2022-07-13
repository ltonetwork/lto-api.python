from freezegun import freeze_time
from lto.transactions.data import Data
from lto.transactions.data import DataEntry
from lto.accounts.ed25519.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from time import time


class TestData:
    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)
    data_entries = {
        "test": 1,
        "second": True
    }

    def test_construct(self):
        transaction = Data(self.data_entries)
        assert (transaction.data[0].key == 'test')
        assert (transaction.data[0].type == 'integer')
        assert (transaction.data[0].value == 1)
        assert (transaction.data[1].key == 'second')
        assert (transaction.data[1].type == 'boolean')
        assert (transaction.data[1].value is True)

    @freeze_time("2021-01-14")
    def test_sign_with(self):
        transaction = Data(self.data_entries)
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
        "type": 12,
        "version": 3,
        "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
        'sender': '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
        'senderKeyType': 'ed25519',
        "fee": 60000000,
        "timestamp": 1610582400000,
        "data": [
            {'key': 'test', 'type': 'integer', 'value': 1},
            {'key': 'second', 'type': 'boolean', 'value': True}
        ],
        "proofs": ['5TeHpP2FdmU9pUxkM2jbDDbqF4P6C1x5Q1KR4xFFQAWWi75enfR3wRhNcvbzraGB6No9HPa7FEjTtdnFbnGaKhJM']
    }

    @freeze_time("2021-01-14")
    def test_to_json(self):
        transaction = Data(self.data_entries)
        assert transaction.version == 3
        transaction.sign_with(self.account)
        json_transaction = transaction.to_json()
        assert json_transaction == self.expected_v3

    def test_from_data(self):
        data = {
            "id": "1uZqDjRjaehEceSxrVxz6WD6wt8su8TBHyDLQ1KFnJo",
            "type": 12,
            "version": 3,
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            'sender': '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            'senderKeyType': 'ed25519',
            "fee": 100000000,
            "timestamp": 1610582400000,
            "data": [
                {'key': 'test', 'type': 'integer', 'value': 1},
                {'key': 'second', 'type': 'boolean', 'value': True}
            ],
            "proofs": ['5TeHpP2FdmU9pUxkM2jbDDbqF4P6C1x5Q1KR4xFFQAWWi75enfR3wRhNcvbzraGB6No9HPa7FEjTtdnFbnGaKhJM'],
            "height": 1225712
        }

        transaction = Data.from_data(data)

        assert transaction.version == 3
        assert transaction.id == "1uZqDjRjaehEceSxrVxz6WD6wt8su8TBHyDLQ1KFnJo"
        assert transaction.sender == "3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2"
        assert transaction.sender_key_type == "ed25519"
        assert transaction.sender_public_key == "4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz"
        assert transaction.fee == 100000000
        assert transaction.timestamp == 1610582400000

        assert len(transaction.data) == 2
        assert transaction.data[0].key == 'test'
        assert transaction.data[0].type == 'integer'
        assert transaction.data[0].value == 1
        assert transaction.data[1].key == 'second'
        assert transaction.data[1].type == 'boolean'
        assert transaction.data[1].value == True

        assert transaction.proofs == [
            "5TeHpP2FdmU9pUxkM2jbDDbqF4P6C1x5Q1KR4xFFQAWWi75enfR3wRhNcvbzraGB6No9HPa7FEjTtdnFbnGaKhJM"
        ]
        assert transaction.height == 1225712
