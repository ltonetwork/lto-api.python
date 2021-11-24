from unittest import mock

import pytest

from lto.transactions.transfer import Transfer
from lto.accounts.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from time import time
from lto import crypto


class TestTransfer:
    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    ACCOUNT2_SEED = "cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)
    account2 = AccountFactory('T').create_from_seed(ACCOUNT2_SEED)


    def test_construct(self):
        transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 10000)
        assert transaction.amount == 10000
        assert transaction.recipient == '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb'
        assert transaction.tx_fee == 100000000

    def test_sign_with(self):
        transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 10000)
        assert transaction.is_signed() is False
        transaction.sign_with(self.account)
        assert transaction.is_signed() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.sender_public_key == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verify_signature(transaction.to_binary(), transaction.proofs[0])

    def test_sign_with_multi_sig(self):
        transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 10000)
        transaction.timestamp = 1629883934685
        transaction.sender = '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        transaction.sender_public_key = '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        transaction.proofs = ['PTEgvxqiUswaKiHoamMpTDRDS6u9msGoS2Hz56c16xSTHRfMnNPgbGBrDtonCspE9RErdsei7RQaFBbPWZgTJbj']

        transaction.sign_with(self.account2)
        assert transaction.is_signed() is True
        assert transaction.timestamp == 1629883934685
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.sender_public_key == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert len(transaction.proofs) == 2
        assert transaction.proofs[
                   0] == 'PTEgvxqiUswaKiHoamMpTDRDS6u9msGoS2Hz56c16xSTHRfMnNPgbGBrDtonCspE9RErdsei7RQaFBbPWZgTJbj'
        assert self.account2.verify_signature(transaction.to_binary(), transaction.proofs[1])


    expected_v2 = {
        "type": 4,
        "version": 2,
        "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
        "recipient": '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb',
        'sender': '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
        "amount": 120000000,
        'senderKeyType': 'ed25519',
        "fee": 100000000,
        "timestamp": 1609773456000,
        "attachment": 'Cn8eVZg',
        "proofs": ['4dcxLgx8gNYnHaAgdjrJ11xjLKanw6pz9PHBr375r13m6evJ5vW6o4Ga7LQGtMj9rwBuGWcCDmUdqa35kn4TLoiC']
    }

    expected_v3 = {
        "type": 4,
        "version": 3,
        "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
        "recipient": '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb',
        "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
        "senderKeyType": 'ed25519',
        "amount": 120000000,
        "fee": 100000000,
        "timestamp": 1609773456000,
        "attachment": 'Cn8eVZg',
        "proofs": ['3Mg3d3wEjtnCjUWguSj1Gir35Dv1xBYHwL3hyfb1iMg2wzGcKtGhfjHoE2BYvsJyodW9g74agBLP2dWNCsVkVour']
    }

    @pytest.mark.parametrize("version, expected", [(2, expected_v2), (3, expected_v3)])
    def test_to_json(self, expected, version):
        transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 120000000, 'hello')
        transaction.timestamp = 1609773456000
        transaction.version = version
        transaction.sign_with(self.account)
        assert transaction.to_json() == expected

    @mock.patch('src.lto.PublicNode')
    def test_broadcast(self, mock_Class):
        transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 120000000, 'Hello')
        broadcastedTransaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 120000000, 'Hello')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction
        assert transaction.broadcast_to(node=mock_Class()) == broadcastedTransaction

    def test_from_data(self):
        data = {
            "id": "5a1ZVJTu8Y7mPA6BbkvGdfmbjvz9YSppQXPnb5MxihV5",
            "type": 4,
            "version": 3,
            "sender": "3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh",
            "senderPublicKey": "9NFb1rvMyr1k8f3wu3UP1RaEGsozBt9gF2CmPMGGA42m",
            "fee": 100000000,
            "timestamp": 1609639213556,
            "amount": 100000000000,
            "recipient": "3NBcx7AQqDopBj3WfwCVARNYuZyt1L9xEVM",
            "attachment": "9Ajdvzr",
            "proofs": [
                "3ftQ2ArKKXw655WdHy2TK1MGXeyzKRqMQYwFidekkyxLpzFGsTziSFsbM5RCFxrn32EzisMgPWtQVQ4e5UqKUcES"
            ],
            "height": 1212761
        }
        transaction = Transfer(recipient=data['recipient'], amount=data['amount']).from_data(data)
        crypto.compare_data_transaction(data, transaction)
