from lto.transactions.mass_transfer import MassTransfer
from lto.accounts.ed25519.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from time import time
from unittest import mock
from lto import crypto
import pytest
from freezegun import freeze_time

class TestMassTransfer:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)
    transfers = ({
                     "recipient": "3HUQa6qtLhNvBJNyPV1pDRahbrcuQkaDQv2",
                     "amount": 100000000
                 }, {
                     "recipient": "3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb",
                     "amount": 200000000
                 })


    def test_construct(self):
        transaction = MassTransfer(self.transfers, attachment='Hello')
        assert transaction.transfers == self.transfers
        assert transaction.BASE_FEE == 100000000
        assert transaction.VAR_FEE == 10000000
        assert transaction.tx_fee == 120000000
        assert transaction.attachment == 'Hello'





    @freeze_time("2021-01-14")
    def test_sign_with(self):
        transaction = MassTransfer(self.transfers, attachment='Hello')
        assert transaction.is_signed() is False
        transaction.sign_with(self.account)
        assert transaction.is_signed() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.sender_public_key == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verify_signature(transaction.to_binary(), transaction.proofs[0])

    expected_v1 = {
            "type": 11,
            "version": 1,
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            'senderKeyType': 'ed25519',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 120000000,
            'height': '',
            'id': '',
            "timestamp": 1326499200000,
            "attachment": '9Ajdvzr',
            'transfers': ({'amount': 100000000,
                           'recipient': '3HUQa6qtLhNvBJNyPV1pDRahbrcuQkaDQv2'},
                          {'amount': 200000000,
                           'recipient': '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb'}),
            "proofs": ['48THooU3mE2NU7TPPeTp8FzRWQ3YUMZFFrUQbVdRkV6xiYoQbJYqZxUc7hhmGJVvKEy93E3g9SKgX5R5BwTkMfYS']
        }

    expected_v3 = {
            "type": 11,
            "version": 3,
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderKeyType": "ed25519",
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 120000000,
            'height': '',
            'id': '',
            "timestamp": 1326499200000,
            "proofs": ['5Sd62Xcjp3rxcwLZShSYWgZ74eWXkdY8cAzyZpd4ejKRXbSNX9a66WrZPc4Vo8VoetqX9jn5wC7e5iyTSc9GC8vg'],
            "attachment": '9Ajdvzr',
            'transfers': ({'amount': 100000000,
                           'recipient': '3HUQa6qtLhNvBJNyPV1pDRahbrcuQkaDQv2'},
                          {'amount': 200000000,
                           'recipient': '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb'})
        }


    @freeze_time("2021-01-14")
    @pytest.mark.parametrize("version, expected", [(1, expected_v1), (3, expected_v3)])
    def test_to_json(self, expected, version):
        transaction = MassTransfer(self.transfers, attachment='Hello')
        transaction.timestamp = 1326499200000
        transaction.version = version
        transaction.sign_with(self.account)
        assert transaction.to_json() == expected

    @mock.patch('src.lto.PublicNode')
    def test_broadcast(self, mock_Class):
        transaction = MassTransfer(self.transfers, attachment='Hello')
        broadcastedTransaction = MassTransfer(self.transfers, attachment='Hello')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction
        assert mc.broadcast(transaction) == broadcastedTransaction


    @freeze_time("2021-01-14")
    def test_from_data(self):
        data = {
              "type" : 11,
              "version" : 3,
              "id" : "BG7MQF8KffVU6MMbJW5xPowVQsohwJhfEJ4wSF8cWdC2",
              "sender" : "3HhQxe5kLwuTfE3psYcorrhogY4fCwz2BSh",
              "senderKeyType": "Ed25519",
              "senderPublicKey" : "7eAkEXtFGRPQ9pxjhtcQtbH889n8xSPWuswKfW2v3iK4",
              "fee" : 200000,
              "timestamp" : 1518091313964,
              "proofs" : [ "4Ph6RpcPFfBhU2fx6JgcHLwBuYSpn..." ],
              "attachment" : "59QuUcqP6p",
              "transfers" : [
                {
                  "recipient" : "3HUQa6qtLhNvBJNyPV1pDRahbrcuQkaDQv2",
                  "amount" : 100000000
                }, {
                  "recipient" : "3HaAdZcCXAqhvFj113Gbe3Kww4rCGMUZaEZ",
                  "amount" : 200000000
                }
              ]
            }
        transaction = MassTransfer(transfers='').from_data(data)
        crypto.compare_data_transaction(data, transaction)

