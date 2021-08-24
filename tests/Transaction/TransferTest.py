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


    def testSign(self):
        transaction = Transfer('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 10000)
        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        #assert transaction.signature == 'fn8c7LUg6pTEkrK9C69E8fhhkdv4jeFrB8qWKfMf51rv79p21DoytK2vH8cJKFVSWE5V2tTrXcFtxbAyg2PXbHo'
        assert self.account.verifySignature(transaction.toBinary(), transaction.signature)
        # how can you access the proofs ? also the signature (proofs) changes every time, how can you check it?
        # why are we checking the timestamps? sometimes the check happens one second later and it throws an error

    def dataProvider(self):
        return ({
            "type": 4,
            "version": 2,
            "senderPublicKey": '7gghhSwKRvshZwwh6sG97mzo1qoFtHEQK7iM4vGcnEt7',
            "recipient": '3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh',
            "amount": 120000000,
            "fee": 100000000,
            "timestamp": 1609773456000,
            "attachment": '9Ajdvzr',
            "proofs": ['57Ysp2ugieiidpiEtutzyfJkEugxG43UXXaKEqzU3c2oLmN8qd3hzEFQoNL93R1SvyXemnnTBNtfhfCM2PenmQqa']
        })

    def TestFromData(self):
        transaction = Transfer('3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh', 120000000, 'Hello')
        transaction.id
