from PyCLTO.AccountFactory import AccountFactory
from PyCLTO.Transactions.Association import Association

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
        transaction.timestamp = 1629883934685
        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])

    def dataProvider(self):
        return ({
            "type": 16,
            "version": 1,
            "party": '3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh',
            "associationType": 42,
            "anchors": '1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 100000000,
            "timestamp": 1610154732000,
            "proofs": ['4NrsjbkkWyH4K57jf9MQ5Ya9ccvXtCg2BQV2LsHMMacZZojbcRgesB1MruVQtCaZdvFSswwju5zCxisG3ZaQ2LKF']
        })