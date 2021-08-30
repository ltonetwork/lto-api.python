from PyCLTO.Transactions.SetScript import SetScript
from PyCLTO.AccountFactory import AccountFactory
from time import time
import copy
from unittest import mock


class TestSetScript:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)

    def testConstruct(self):
        transaction = SetScript(b'aGVsbG8=')
        assert transaction.script == b'aGVsbG8='
        assert transaction.txFee == 500000000


    def testSignWith(self):
        transaction = SetScript(b'aGVsbG8=')
        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])

    def testToJson(self):
        transaction = SetScript(b'aGVsbG8=')
        transaction.timestamp = 1609773456000
        transaction.signWith(self.account)

        expected = {
            "type": 13,
            "version": 1,
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 500000000,
            "timestamp": 1609773456000,
            "script": 'base64:' + str(b'aGVsbG8='),
            "proofs": ['2vjigxGPYFna9rhMSjRkbtPeS9LJLbM1C3VNpS85bxQEUUftmvX7hNqFoy8Su2eiE75BMAqmtfKocvy275xj14xm']
        }
        assert transaction.toJson() == expected

    @mock.patch('PyCLTO.PublicNode')
    def testBroadcast(self, mock_Class):
        transaction = SetScript(b'aGVsbG8=')
        broadcastedTransaction = copy.copy(transaction)
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'

        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction

        assert mc.broadcast(transaction) == broadcastedTransaction





