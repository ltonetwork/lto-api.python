from LTO.Transactions.MassTransfer import MassTransfer
from LTO.AccountFactory import AccountFactory
from time import time
import copy
from unittest import mock

class TestMassTransfer:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)
    transfers = ({
                     "recipient": "3HUQa6qtLhNvBJNyPV1pDRahbrcuQkaDQv2",
                     "amount": 100000000
                 }, {
                     "recipient": "3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb",
                     "amount": 200000000
                 })


    def testConstruct(self):
        transaction = MassTransfer(self.transfers, attachment='Hello')
        assert transaction.transfers == self.transfers
        assert transaction.baseFee == 100000000
        assert transaction.txFee == 120000000
        assert transaction.attachment == 'Hello'





    def testSignWith(self):
        transaction = MassTransfer(self.transfers, attachment='Hello')
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
            "type": 11,
            "version": 1,
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 120000000,
            "timestamp": 1609773456000,
            "attachment": '9Ajdvzr',
            'transfers': ({'amount': 100000000,
                           'recipient': '3HUQa6qtLhNvBJNyPV1pDRahbrcuQkaDQv2'},
                          {'amount': 200000000,
                           'recipient': '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb'}),
            "proofs": ['4AtTkZ4caFohQhLcDa4qKVLQ7tMFwKuDAdFnZHz3D7kHnLVytKxLxKETbAqyEB9tZQ6NDPwnfkY65wptfB8xK3xm']
        }

    def expectedV3(self):
        return {
            "type": 11,
            "version": 3,
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderKeyType": "ed25519",
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 120000000,
            "timestamp": 1609773456000,
            "proofs": ['3LBJB599XrpYE5NV5TLRKfYZ33ZubTNepgzabFuxAXrS2GE9UnN6UTxQjbgjG2zmkapsGaT8ucbngd3JsNUR2vSh'],
            "attachment": '9Ajdvzr',
            'transfers': ({'amount': 100000000,
                           'recipient': '3HUQa6qtLhNvBJNyPV1pDRahbrcuQkaDQv2'},
                          {'amount': 200000000,
                           'recipient': '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb'})
        }

    def testToJson(self):
        transaction = MassTransfer(self.transfers, attachment='Hello')
        transaction.timestamp = 1609773456000
        transaction.signWith(self.account)
        if transaction.version == 1:
            expected = self.expectedV1()
        elif transaction.version == 3:
            expected = self.expectedV3()
        else:
            expected = ''

        assert transaction.toJson() == expected

    @mock.patch('LTO.PublicNode')
    def testBroadcast(self, mock_Class):
        transaction = MassTransfer(self.transfers, attachment='Hello')
        broadcastedTransaction = MassTransfer(self.transfers, attachment='Hello')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction
        assert mc.broadcast(transaction) == broadcastedTransaction


    def testFromData(self):
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
        transaction = MassTransfer(transfers='').fromData(data)
        for key in data:
            assert data[key] == transaction.__getattr__(key)

