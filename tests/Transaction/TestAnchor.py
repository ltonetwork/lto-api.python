from PyCLTO.AccountFactory import AccountFactory
from PyCLTO.Transactions.Anchor import anchor

class TestAnchor:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)

    def testContruct(self):
        transaction = anchor('1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89')
        assert transaction.txFee == 35000000
        assert transaction.anchor == '1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89'


    def testSignWith(self):
        transaction = anchor('1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89')
        transaction.timestamp = 1629883934685
        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])

    def dataProvider(self):
        return ({
            "type": 15,
            "version": 1,
            "anchors": '1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 35000000,
            "timestamp": 1609773456000,
            "proofs": ['PTEgvxqiUswaKiHoamMpTDRDS6u9msGoS2Hz56c16xSTHRfMnNPgbGBrDtonCspE9RErdsei7RQaFBbPWZgTJbj']
        })


    def TestToJson(self):
        transaction = anchor('1e00e94a90a69a52eea88b2179ef0d1728f82361a56f0b379ce1fab9d8d86a89')
        transaction.timestamp = 1609773456000
        transaction.signWith(self.account)
        ret = self.dataProvider()
        json = transaction.toJson()
        assert json['type'] == ret['type']
        assert json['version'] == ret['version']
        assert json['senderPublicKey'] == ret['senderPublicKey']
        assert json['anchors'] == ret['anchors']
        assert json['fee'] == ret['fee']
        assert json['timestamp'] == ret['timestamp']
        assert json['proofs'] == ret['proofs']
