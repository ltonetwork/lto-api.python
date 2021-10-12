from LTO.Transactions.Lease import Lease
from LTO.Accounts.AccountFactoryED25519 import AccountED25519 as AccountFactory
from time import time
from unittest import mock

class TestLease:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)

    def testConstruct(self):
        transaction = Lease('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 10000)
        assert transaction.amount == 10000
        assert transaction.recipient == '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb'
        assert transaction.txFee == 100000000


    def testSignWith(self):
        transaction = Lease('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 10000)
        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])

    def expectedV2(self):
        return {
            "type": 8,
            "version": 2,
            'sender': '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "recipient": '3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh',
            "amount": 120000000,
            "fee": 100000000,
            "timestamp": 1609773456000,
            "proofs": ['4EMRcCDE6ihnoQht5VHe8sNK2RGdhKfCXBWFy1Vt1Qr76Sd7h1Y25YSBwNLLcZuqvHBcMQQge6mLw4b8Nu4YMjWa']
        }

    def expectedV3(self):
        return {
            "type": 8,
            "version": 3,
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderKeyType": "ed25519",
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "recipient": '3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh',
            "amount": 120000000,
            "fee": 100000000,
            "timestamp": 1609773456000,
            "proofs": ['2BmzCScRy6soyyufzxkNRc3kATCh3HYPtNsGb2Nx6RTkNWXGwMFQLj5cCzKZhJG9TxQHu4DFQyeEuNinJnXC3Ft7']
        }

    def testToJson(self):
        transaction = Lease('3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh', 120000000)
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
        transaction = Lease('3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh', 120000000)
        broadcastedTransaction = transaction
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction
        assert mc.broadcast(transaction) == broadcastedTransaction

    def testFromData(self):
        data = {
            "id": "895ryYABK7KQWLvSbw8o8YSjTTXHCqRJw1yzC63j4Fgk",
            "type" : 8,
            "version": 3,
            "sender" : "3HgqG68qfeVz5dqbyvqnxQceFaH49xmGvUS",
            "senderKeyType": 'ed25519',
            "senderPublicKey" : "DddGQs63eWAA1G1ZJnJDVSrCpMS97NH4odnggwUV42kE",
            "fee" : 500000000,
            "timestamp" : 1495625418143,
            "proofs" : "2SUmFj4zo7NfZK7Xoqvqh7m7bhzFR8rT7eLtqe9Rrp18ugFH9SSvoTx1BtekWhU7PN1uLrnQCpJdS8JhmcBAjmb9",
            "recipient": "3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb"
        }
        transaction = Lease(amount=1, recipient='3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb').fromData(data)
        for key in data:
            assert data[key] == transaction.__getattr__(key)


