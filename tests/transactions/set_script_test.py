from lto.transactions.set_script import SetScript
from lto.accounts.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from time import time
from unittest import mock
from lto import crypto


class TestSetScript:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)

    def test_construct(self):
        transaction = SetScript(b'aGVsbG8=')
        assert transaction.script == b'aGVsbG8='
        assert transaction.tx_fee == 500000000


    def test_sign_with(self):
        transaction = SetScript(b'aGVsbG8=')
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
            "type": 13,
            "version": 1,
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 500000000,
            "timestamp": 1609773456000,
            "script": 'base64:' + str(b'aGVsbG8='),
            "proofs": ['Z5dX5Upqq8ergHPhi4J2qLTroLKzUUdf3yR36Ns9oiASs6nWKdDHacD4W2WzweQczJaUCogrBZ6xMhMi1vKMXky']
        }

    def expected_v3(self):
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

    def test_to_json(self):
        transaction = SetScript(b'aGVsbG8=')
        transaction.timestamp = 1609773456000
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
        transaction = SetScript(b'aGVsbG8=')
        broadcastedTransaction = SetScript(b'aGVsbG8=')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'

        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction

        assert mc.broadcast(transaction) == broadcastedTransaction


    def test_from_data(self):
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
        transaction = SetScript(data['script']).from_data(data)
        crypto.compare_data_transaction(data, transaction)


