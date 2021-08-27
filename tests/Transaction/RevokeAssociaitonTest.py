from PyCLTO.Transactions.RevokeAssociation import RevokeAssociation
from PyCLTO.AccountFactory import AccountFactory
from time import time


class TestRevokeAssociation:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)

    def testConstruct(self):
        transaction = RevokeAssociation('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 42)
        assert transaction.party == '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1'
        assert transaction.associationType == 42
        assert transaction.txFee == 100000000


    def testSignWith(self):
        transaction = RevokeAssociation('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 42, anchor='3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
        transaction.timestamp = 1629883934685

        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        assert transaction.anchor == '3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj'
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])


    def dataProvider(self):
        return ({
            "type": 17,
            "version": 1,
            "sender": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "hash": 'Hjh8aEYykDxvjksNKKM2SSun3nAmXvjg5cT8zqXubqrZPburn9qYebuJ5cFb',
            "associationType": 42,
            "party": '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
            "fee": 100000000,
            "timestamp": 1609773456000,
            "proofs": ['ei6KMhNZKtfSCJWrWmmUcpmDw5eL8uqwMiHkMKUVcmHykGgrYAKdEJ54cDVKhSXmzeybTEasW6kUaKSRWCwAgf9']
        })


    def testToJson(self):
        transaction = RevokeAssociation('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 42, '3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
        transaction.timestamp = 1609773456000
        transaction.signWith(self.account)
        assert transaction.toJson() == self.dataProvider()




