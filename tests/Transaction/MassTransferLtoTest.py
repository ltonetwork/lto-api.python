from PyCLTO.Transactions.MassTransferLto import MassTransferLTO
from PyCLTO.AccountFactory import AccountFactory
from time import time
import copy
from unittest import mock

class TestMassTransferLTO:

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
        transaction = MassTransferLTO(self.transfers, attachment='Hello')
        assert transaction.transfers == self.transfers
        assert transaction.baseFee == 100000000
        assert transaction.txFee == 120000000
        assert transaction.attachment == 'Hello'




    def testSignWith(self):
        transaction = MassTransferLTO(self.transfers, attachment='Hello')
        transaction.timestamp = 1629883934685

        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])


    def dataProvider(self):
        return ({
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
        })


    def testToJson(self):
        transaction = MassTransferLTO(self.transfers, attachment='Hello')
        transaction.timestamp = 1609773456000
        transaction.signWith(self.account)
        assert transaction.toJson() == self.dataProvider()




