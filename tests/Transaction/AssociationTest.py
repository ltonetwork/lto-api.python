from PyCLTO.AccountFactory import AccountFactory
from PyCLTO.Transactions.Association import Association
import copy
from unittest import mock
from time import time

class TestAssociation:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)

    def testContruct(self):
        transaction = Association('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 42)
        assert transaction.txFee == 100000000
        assert transaction.associationType == 42
        assert transaction.party == '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1'


    def testSignWith(self):
        transaction = Association('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 42)
        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])


    def testToJson(self):
        transaction = Association('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 42, anchor='3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        transaction.timestamp = 1629883934685
        transaction.signWith(self.account)
        expected = {
            "type": 16,
            "version": 1,
            "party": '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
            "associationType": 42,
            "hash": 'HiorsQW6E76Cp4AD51zcKcWu644ZzzraXQL286Jjzufh7U7qJroTKt7KMMpv',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 100000000,
            "timestamp": 1629883934685,
            "proofs": ['2wVY2YatNA72rLYuQ4vdpYKLJSPbJ9LewwEmr8vFJHBRBjkmnqd8GhVmFRd4jtYLUGJeiV7V9HkVYPN1bs8siyts']
            }
        assert transaction.toJson() == expected

    @mock.patch('PyCLTO.PublicNode')
    def testBroadcast(self, mock_Class):
        transaction = Association('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 42, anchor='3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        broadcastedTransaction = copy.copy(transaction)
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction
        assert mc.broadcast(transaction) == broadcastedTransaction