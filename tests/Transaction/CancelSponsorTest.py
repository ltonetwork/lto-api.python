from PyCLTO.Transactions.CancelSponsor import CancelSponsor
from PyCLTO.AccountFactory import AccountFactory
from time import time
import copy
from unittest import mock

class TestCancelSponsor:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)

    def testConstruct(self):
        transaction = CancelSponsor('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1')
        assert transaction.recipient == '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1'
        assert transaction.txFee == 500000000


    def testSignWith(self):
        transaction = CancelSponsor('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1')
        transaction.timestamp = 1629883934685

        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])


    def dataProvider(self):
        return ({
            "type": 19,
            "version": 1,
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "recipient": '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
            "fee": 500000000,
            "timestamp": 1609773456000,
            "proofs": ['3XpCsLdZQHnM6o9gKw3hU6rVj2W9R4NZuZAmWdvBDgv69ikzoQVnQBo9hx3udz6khnbgdU1ivrDmhysnA1rmEUV3']
        })


    def testToJson(self):
        transaction = CancelSponsor('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1')
        transaction.timestamp = 1609773456000
        transaction.signWith(self.account)
        assert transaction.toJson() == self.dataProvider()




