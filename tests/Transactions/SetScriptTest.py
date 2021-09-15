from src.LTO.Transactions.SetScript import SetScript
from src.LTO.AccountFactory import AccountFactory
from time import time
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

    def expectedV1(self):
        return {
            "type": 13,
            "version": 1,
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 500000000,
            "timestamp": 1609773456000,
            "script": 'base64:' + str(b'aGVsbG8='),
            "proofs": ['Z5dX5Upqq8ergHPhi4J2qLTroLKzUUdf3yR36Ns9oiASs6nWKdDHacD4W2WzweQczJaUCogrBZ6xMhMi1vKMXky']
        }

    def expectedV3(self):
        return {
            "type": 13,
            "version": 3,
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderKeyType": "ed25519",
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 500000000,
            "timestamp": 1609773456000,
            "script": 'base64:' + str(b'aGVsbG8='),
            "proofs": ['219nTCZuFxcYFew6KSg2d4Udhm1bMZKJTmBemoVYbHScp38FFof8tV4vu9jVqNndVvK1Xo5R5XACJNSWtvUuSJXG']
        }

    def testToJson(self):
        transaction = SetScript(b'aGVsbG8=')
        transaction.timestamp = 1609773456000
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
        transaction = SetScript(b'aGVsbG8=')
        broadcastedTransaction = SetScript(b'aGVsbG8=')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'

        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction

        assert mc.broadcast(transaction) == broadcastedTransaction


    def testFromData(self):
        data = {
            "type": 13,
            "version": 1,
            "id": 'BG7MQF8KffVU6MMbJW5xPowVQsohwJhfEJ4wSF8cWdC2',
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderKeyType": "ed25519",
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 500000000,
            "timestamp": 1609773456000,
            "script": b'aGVsbG8=',
            "proofs": ['2vjigxGPYFna9rhMSjRkbtPeS9LJLbM1C3VNpS85bxQEUUftmvX7hNqFoy8Su2eiE75BMAqmtfKocvy275xj14xm']
        }
        transaction = SetScript(data['script']).fromData(data)
        for key in data:
            assert data[key] == transaction.__getattr__(key)


