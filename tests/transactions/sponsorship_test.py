from lto.accounts.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from lto.transactions.sponsorship import Sponsorship
from unittest import mock
from time import time
from lto import crypto

class TestSponsorship:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)

    def test_construct(self):
        transaction = Sponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        assert transaction.tx_fee == 500000000
        assert transaction.recipient == '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb'


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


    def expected_v1(self):
        return {
            "type": 18,
            "version": 1,
            "recipient": '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb',
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 500000000,
            "timestamp": 1610142631066,
            "proofs": ['zqoN7PBwnRvYP72csdoszjz11u6HR2ogoomrgF8d7Aky8CR6eqM1PUM36EFnvbrKmpoLccDKmKTw4fX34xSPEvH']
        }

    def expected_v3(self):
        return {
            "type": 18,
            "version": 3,
            "senderKeyType": "ed25519",
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "recipient": '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb',
            "timestamp": 1610142631066,
            "fee": 500000000,
            "proofs": ['4MKFzXKpgRxzLGJnCPsYzUePd7NjzVtE7uD1EsYeK4q1NmHDUgMfVHYStDJU3dUyTSptS7otGKxfXkxVFUJvKers']
        }

    def test_to_json(self):
        transaction = Sponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        transaction.timestamp = 1610142631066
        transaction.sign_with(self.account)
        if transaction.version == 1:
            expected = self.expected_v1()
        elif transaction.version == 3:
            expected = self.expected_v3()
        else:
            expected = ''

        assert transaction.to_json() == expected

    @mock.patch('src.lto.PublicNode')
    def test_broadcast(self, mock_Class):
        transaction = Sponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        broadcastedTransaction = Sponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'

        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction

        assert mc.broadcast(transaction) == broadcastedTransaction

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
