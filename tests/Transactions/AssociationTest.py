from LTO.Accounts.AccountFactoryED25519 import AccountFactoryED25519 as AccountFactory
from LTO.Transactions.Association import Association
from unittest import mock
from time import time

class TestAssociation:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)

    def testContruct(self):
        transaction = Association('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1)
        assert transaction.txFee == 100000000
        assert transaction.associationType == 1
        assert transaction.recipient == '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1'


    def testSignWith(self):
        transaction = Association('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1)
        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])


    def expectedV1(self):
        return({'associationType': 1,
                'fee': 100000000,
                'hash': 'HiorsQW6E76Cp4AD51zcKcWu644ZzzraXQL286Jjzufh7U7qJroTKt7KMMpv',
                'proofs': ['3pX89U3uEYV2MA5gJWDsXRWC8Wnynd9T4X6LraQr7eNL1KmcgBiMxaT4adKqsYZMFxGTc5mpNao9WTziNTndLLEQ'],
                'recipient': '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
                'sender': '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
                'senderPublicKey': '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
                'timestamp': 1629883934685,
                'type': 16,
                'version': 1})


    def expectedV3(self):
        return({
            "type": 16,
            "version": 3,
            "sender": "3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2",
            "senderKeyType": "ed25519",
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "recipient": '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
            "associationType": 1,
            "hash": 'HiorsQW6E76Cp4AD51zcKcWu644ZzzraXQL286Jjzufh7U7qJroTKt7KMMpv',
            "timestamp": 1629883934685,
            "expires": 1841961856000,
            "fee": 100000000,
            "proofs": ['2Mhouk8hgCSALbDKZhCCDVuMoN8PmwUEWWtzaPmbY3CPDbEutAqoyDbZDsdWfkRyrBUnHSJ3XDfZfHwps5z1b6Qr'],
        })


    def testToJson(self):
        transaction = Association('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1, anchor='3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk', expires= 1841961856000)
        #transaction = Association('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1, anchor='3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk', expires=1841961856000)
        transaction.timestamp = 1629883934685
        transaction.signWith(self.account)

        if transaction.version == 1:
            expected = self.expectedV1()
        elif transaction.version == 3:
            expected = self.expectedV3()
        else:
            expected = ''

        assert transaction.toJson() == expected

    @mock.patch('src.LTO.PublicNode')
    def testBroadcast(self, mock_Class):
        transaction = Association('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1, anchor='3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        broadcastedTransaction = Association('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1, anchor='3mM7VirFP1LfJ5kGeWs9uTnNrM2APMeCcmezBEy8o8wk')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction
        assert mc.broadcast(transaction) == broadcastedTransaction

    def testFromData(self):
        data = {
            "type": 16,
            "version": 3,
            "recipient": "3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh",
            "associationType": 1,
            "hash": "3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj",
            "id": "1uZqDjRjaehEceSxrVxz6WD6wt8su8TBHyDLQ1KFnJo",
            "sender": "3NBcx7AQqDopBj3WfwCVARNYuZyt1L9xEVM",
            "senderPublicKey": "7gghhSwKRvshZwwh6sG97mzo1qoFtHEQK7iM4vGcnEt7",
            "timestamp": 1610404930000,
            "expires": 1841961856000,
            "fee": 100000000,
            "proofs": [
                "2jQMruoLoshfKe6FAUbA9vmVVvAt8bVpCFyM75Z2PLJiuRmjmLzFpM2UmgQ6E73qn46AVQprQJPBhQe92S7iSXbZ"
            ],
            "height": 1225712
        }
        transaction = Association(recipient='', associationType='').fromData(data)

        for key in data:
            assert data[key] == transaction.__getattr__(key)
