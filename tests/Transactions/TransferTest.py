from unittest import mock
from LTO.Transactions.Transfer import Transfer
from LTO.Accounts.AccountFactoryED25519 import AccountFactoryED25519 as AccountFactory
from time import time


class TestTransfer:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    ACCOUNT2_SEED = "cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)
    account2 = AccountFactory('T').createFromSeed(ACCOUNT2_SEED)


    def testConstruct(self):
        transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 10000)
        assert transaction.amount == 10000
        assert transaction.recipient == '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb'
        assert transaction.txFee == 100000000


    def testSignWith(self):
        transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 10000)
        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])


    def testSignWithMultisig(self):
        transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 10000)
        transaction.timestamp = 1629883934685
        transaction.sender = '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        transaction.senderPublicKey = '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        transaction.proofs = ['PTEgvxqiUswaKiHoamMpTDRDS6u9msGoS2Hz56c16xSTHRfMnNPgbGBrDtonCspE9RErdsei7RQaFBbPWZgTJbj']

        transaction.signWith(self.account2)
        assert transaction.isSigned() is True
        assert transaction.timestamp == 1629883934685
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert len(transaction.proofs) == 2
        assert transaction.proofs[0] == 'PTEgvxqiUswaKiHoamMpTDRDS6u9msGoS2Hz56c16xSTHRfMnNPgbGBrDtonCspE9RErdsei7RQaFBbPWZgTJbj'
        assert self.account2.verifySignature(transaction.toBinary(), transaction.proofs[1])

    def expectedV2(self):
        return({
            "type": 4,
            "version": 2,
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "recipient": '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb',
            'sender': '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "amount": 120000000,
            "fee": 100000000,
            "timestamp": 1609773456000,
            "attachment": '9Ajdvzr',
            "proofs": ['QJXntVh9422tFcFgzM6edXdVGdcvd9GU35S6FGQSRZKwSqG6PYmf9dsHwdXgKqdDX6m3NrxKQQcCy4yjMZHhaAS']
        })

    def expectedV3(self):
        return({
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
        })


    def testToJson(self):
        transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 120000000, 'hello')
        transaction.timestamp = 1609773456000
        transaction.signWith(self.account)

        if transaction.version == 2:
            expected = self.expectedV2()
        elif transaction.version == 3:
            expected = self.expectedV3()
        else:
            expected = ''

        assert transaction.toJson() == expected


    @mock.patch('src.LTO.PublicNode')
    def testBroadcast(self, mock_Class):
        transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 120000000, 'Hello')
        broadcastedTransaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 120000000, 'Hello')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction
        assert transaction.broadcastTo(node=mock_Class()) == broadcastedTransaction

    def testFromData(self):
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
        transaction = Transfer(recipient=data['recipient'], amount=data['amount']).fromData(data)
        for key in data:
            assert data[key] == transaction.__getattr__(key)




