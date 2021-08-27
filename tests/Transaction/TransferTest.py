from PyCLTO.Transactions.Transfer import Transfer
from PyCLTO.AccountFactory import AccountFactory
from time import time


class TestTransfer:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)

    def testConstruct(self):
        transaction = Transfer('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 10000)
        assert transaction.amount == 10000
        assert transaction.recipient == '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1'
        assert transaction.txFee == 100000000


    def testSignWith(self):
        transaction = Transfer('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 10000)
        transaction.timestamp = 1629883934685

        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])


    def dataProvider(self):
        return ({
            "type": 4,
            "version": 2,
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "recipient": '3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh',
            "amount": 120000000,
            "fee": 100000000,
            "timestamp": 1609773456000,
            "attachment": '9Ajdvzr',
            "proofs": ['PTEgvxqiUswaKiHoamMpTDRDS6u9msGoS2Hz56c16xSTHRfMnNPgbGBrDtonCspE9RErdsei7RQaFBbPWZgTJbj']
        })

    def testToJson(self):
        transaction = Transfer('3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh', 120000000, 'Hello')
        transaction.timestamp = 1609773456000
        transaction.signWith(self.account)
        assert transaction.toJson() == self.dataProvider()
        '''ret = self.dataProvider()
        json = transaction.toJson()
        assert json['type'] == ret['type']
        assert json['version'] == ret['version']
        assert json['senderPublicKey'] == ret['senderPublicKey']
        assert json['recipient'] == ret['recipient']
        assert json['amount'] == ret['amount']
        assert json['fee'] == ret['fee']
        assert json['timestamp'] == ret['timestamp']
        assert json['attachment'] == ret['attachment']
        assert json['proofs'] == ret['proofs']'''




