from lto.accounts.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from lto.transactions.sponsorship import Sponsorship
from unittest import mock
from time import time
from lto import crypto
import pytest
from freezegun import freeze_time

class TestSponsorship:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)

    def test_construct(self):
        transaction = Sponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        assert transaction.tx_fee == 500000000
        assert transaction.recipient == '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb'


    @freeze_time("2021-01-14")
    def test_sign_with(self):
        transaction = Sponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        assert transaction.is_signed() is False
        transaction.sign_with(self.account)
        assert transaction.is_signed() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.sender_public_key == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verify_signature(transaction.to_binary(), transaction.proofs[0])


    expected_v1 = {
            "type": 18,
            "version": 1,
            "recipient": '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb',
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 500000000,
            'senderKeyType': 'ed25519',
            "timestamp": 1326499200000,
            "proofs": ['3gEX99xgnNbbbTVsqZ2mVc1ed1pcAzsAmVoxTXYmhY2xnANNW9NoxXsLyy2m5xot2qXhXb5ZHgL6ZmeYeB1CctWe']
        }

    expected_v3 = {
            "type": 18,
            "version": 3,
            "senderKeyType": "ed25519",
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "recipient": '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb',
            "timestamp": 1326499200000,
            "fee": 500000000,
            "proofs": ['3tTspKV5QemQsxPwoUttaLc7UabQquhSxw1m8qgA9ugiEuDJp2mV2hbcp1C959VrJ1iG8bNgnrTC55E43MDYqPqa']
        }

    @freeze_time("2021-01-14")
    @pytest.mark.parametrize("version, expected", [(1, expected_v1), (3, expected_v3)])
    def test_to_json(self, expected, version):
        transaction = Sponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        transaction.timestamp = 1326499200000
        transaction.version = version
        transaction.sign_with(self.account)
        assert transaction.to_json() == expected

    @mock.patch('src.lto.PublicNode')
    def test_broadcast(self, mock_Class):
        transaction = Sponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        broadcastedTransaction = Sponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'

        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction

        assert mc.broadcast(transaction) == broadcastedTransaction

    @freeze_time("2021-01-14")
    def test_from_data(self):
        data = {
            "type": 18,
            "version": 1,
            "id": "8S2vD5dGCPhwS8jLzNQpSRYDBGXv6GKq6qT5yXUBWPgb",
            "sender": "3NBcx7AQqDopBj3WfwCVARNYuZyt1L9xEVM",
            "senderPublicKey": "7gghhSwKRvshZwwh6sG97mzo1qoFtHEQK7iM4vGcnEt7",
            "recipient": "3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh",
            "timestamp": 1610410901000,
            "fee": 500000000,
            "proofs": [
                "QKef6R8LrMBupBF9Ry8zjFTu3mexC55J6XNofDDQEcJnZJsRjZPnAk6Yn2eiHkqqd2uSjB2r58fC8QVLaVegQEz"
            ],
            "height": 1225821
        }
        transaction = Sponsorship(data['recipient']).from_data(data)
        crypto.compare_data_transaction(data, transaction)
