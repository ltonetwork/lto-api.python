from unittest import mock
import pytest
from freezegun import freeze_time
from lto.transactions.data import Data
from lto.transactions.data import DataEntry
from lto.accounts.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from time import time
from lto import crypto


class TestData:
    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    ACCOUNT2_SEED = "cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)
    account2 = AccountFactory('T').create_from_seed(ACCOUNT2_SEED)
    data_entries = {
        "test": 1,
        "second": True
    }

    def test_construct(self):
        transaction = Data(self.data_entries)
        data_objects = transaction.data
        assert (data_objects[0].key == 'test')
        assert (data_objects[0].type == 'integer')
        assert (data_objects[0].value == 1)
        assert (data_objects[1].key == 'second')
        assert (data_objects[1].type == 'boolean')
        assert (data_objects[1].value is True)

    @freeze_time("2021-01-14")
    def test_sign_with(self):
        transaction = Data(self.data_entries)
        assert transaction.is_signed() is False
        transaction.sign_with(self.account)
        assert transaction.is_signed() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.sender_public_key == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verify_signature(transaction.to_binary(), transaction.proofs[0])

    expected_v1 = {
        "type": 12,
        "version": 1,
        "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
        'sender': '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
        'senderKeyType': 'ed25519',
        "fee": 35000000,
        "timestamp": 1610582400000,
        "proofs": ['3rdaiE7UTS8ChSELdMo2BHFxNzLn4WqKaCBAhdkWxPq6oxFAnqYy47mmRf8M8Nf26UNPRhq22UrQPW1seZ4z975P']
    }

    @freeze_time("2021-01-14")
    @pytest.mark.parametrize("version, expected", [(1, expected_v1)])
    def test_to_json(self, expected, version):
        transaction = Data(self.data_entries)
        transaction.version = version
        transaction.sign_with(self.account)
        json_transaction = transaction.to_json()
        map = json_transaction.pop('data')
        assert json_transaction == expected
        assert map == [{'key': 'test', 'type': 'integer', 'value': 1},
                        {'key': 'second', 'type': 'boolean', 'value': True}]


    def test_from_data(self):
        data = [{'key': 'test', 'type': 'integer', 'value': 1},
                        {'key': 'second', 'type': 'boolean', 'value': True}]
        for entry in data:
            ret = DataEntry.from_data(entry)
            for key in entry:
                assert getattr(ret, key) == entry[key]


