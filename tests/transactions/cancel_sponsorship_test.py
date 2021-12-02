from lto.transactions.cancel_sponsorship import CancelSponsorship
from lto.accounts.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from time import time
from unittest import mock
from lto import crypto
import pytest
from freezegun import freeze_time

class TestCancelSponsorship:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)

    def test_construct(self):
        transaction = CancelSponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        assert transaction.recipient == '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb'
        assert transaction.tx_fee == 500000000


    @freeze_time("2021-01-14")
    def test_sign_with(self):
        transaction = CancelSponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        assert transaction.is_signed() is False
        transaction.sign_with(self.account)
        assert transaction.is_signed() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.sender_public_key == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verify_signature(transaction.to_binary(), transaction.proofs[0])

    expected_v1 = {
            "type": 19,
            "version": 1,
            'senderKeyType': 'ed25519',
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "recipient": '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb',
            "fee": 500000000,
            "timestamp": 1326499200000,
            "proofs": ['5Er5Hfji81xZ2U3rM81Pbmov1smVcfzdoXyjvABv6id4JT9Snhb4UKG9kfxE5KMwuKfjMup3vcgckTTRhx9WKSKE']
        }


    expected_v3 = {
            'fee': 500000000,
            'proofs': ['4gUiQKw6s3odnZY1VutKTT1S3t6RggVqPjEpfwpwCBLuULH5doR1BN2P4VSztoLWAaVjPVQXC62sesaPL6Ufu8uX'],
            'recipient': '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb',
            'sender': '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            'senderKeyType': 'ed25519',
            'senderPublicKey': '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            'timestamp': 1326499200000,
            'type': 19,
            'version': 3
        }



    @freeze_time("2021-01-14")
    @pytest.mark.parametrize("version, expected", [(1, expected_v1), (3, expected_v3)])
    def test_to_json(self, expected, version):
        transaction = CancelSponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        transaction.timestamp = 1326499200000
        transaction.version = version
        transaction.sign_with(self.account)
        assert transaction.to_json() == expected

    @mock.patch('src.lto.PublicNode')
    def test_broadcast(self, mock_Class):
        transaction = CancelSponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        broadcastedTransaction = CancelSponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction
        assert mc.broadcast(transaction) == broadcastedTransaction

    @freeze_time("2021-01-14")
    def test_from_data(self):
        data = {
            "type": 19,
            "version": 3,
            "recipient": "3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh",
            "id": "53r3mwknCUJmyacf1TP1A5zUGCF9z3N951Zegs9UrkZD",
            "sender": "3NBcx7AQqDopBj3WfwCVARNYuZyt1L9xEVM",
            "senderKeyType": "ed25519",
            "senderPublicKey": "7gghhSwKRvshZwwh6sG97mzo1qoFtHEQK7iM4vGcnEt7",
            "timestamp": 1610412950000,
            "fee": 500000000,
            "proofs": [
                "RexaACH8AVfNKQcKDRVCvF2nSAzJLZPyUTtD9KmtikBy5CVCpVeBp78m2Myy7ekkecDMaJwERjgTVxjSxeLd8Da"
            ],
            "height": 1225860
        }
        transaction = CancelSponsorship(data['recipient']).from_data(data)
        crypto.compare_data_transaction(data, transaction)



