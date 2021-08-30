from PyCLTO.AccountFactory import AccountFactory
from PyCLTO.Transactions.Sponsor import Sponsor
import json
import copy
from unittest import mock

class TestSponsor:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)

    def testContruct(self):
        transaction = Sponsor('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1')
        assert transaction.txFee == 500000000
        assert transaction.recipient == '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1'


    def testSignWith(self):
        transaction = Sponsor('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1')
        transaction.timestamp = 1629883934685
        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])

    def dataProvider(self):
        return ({
            "type": 18,
            "version": 1,
            "recipient": '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 500000000,
            "timestamp": 1610142631066,
            "proofs": ['dpqYutUiVoCNdaMGK8rXLSoourUsoHNGANYV2W68mT8aqKEKeZaWZJXs2cN1YQ9fxP6Chcpn1stxr5omGx6Y3Lg']
        })


    def testToJson(self):
        transaction = Sponsor('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1')
        transaction.timestamp = 1610142631066
        transaction.signWith(self.account)
        assert transaction.toJson() == self.dataProvider()

