from LTO.Accounts.AccountFactoryED25519 import AccountFactoryED25519 as AccountFactory
from LTO.Transactions.Sponsorship import Sponsorship
from unittest import mock
from time import time

class TestSponsorship:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)

    def testContruct(self):
        transaction = Sponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        assert transaction.txFee == 500000000
        assert transaction.recipient == '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb'


    def testSignWith(self):
        transaction = Sponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])


    def expectedV1(self):
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

    def expectedV3(self):
        return {
            "type": 18,
            "version": 3,
            "senderKeyType": "ed25519",
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "recipient": '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb',
            "timestamp": 1610142631066,
            "fee": 500000000,
            "proofs": ['64v3hJ99qf8sZt5VnkTaiXbWzjvyTwBVuz7WKM81G5anhfB8rXfWSLo8ci6FCMHQkKMRS725g2zU7tKPTqTfREbR']
        }

    def testToJson(self):
        transaction = Sponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        transaction.timestamp = 1610142631066
        transaction.signWith(self.account)
        if transaction.version == 1:
            expected = self.expectedV1()
        elif transaction.version == 3:
            expected = self.expectedV3()
        else:
            expected = ''

        assert transaction.toJson() == expected

    @mock.patch('src.LTO.PublicNode')
    def testBroadcast(self, mock_Class):
        transaction = Sponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        broadcastedTransaction = Sponsorship('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'

        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction

        assert mc.broadcast(transaction) == broadcastedTransaction

    def testFromData(self):
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
        transaction = Sponsorship(data['recipient']).fromData(data)
        for key in data:
            assert data[key] == transaction.__getattr__(key)
