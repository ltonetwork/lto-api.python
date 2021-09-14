from LTO.Transactions.RevokeAssociation import RevokeAssociation
from LTO.AccountFactory import AccountFactory
from time import time
import copy
from unittest import mock

class TestRevokeAssociation:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)

    def testConstruct(self):
        transaction = RevokeAssociation('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1)
        assert transaction.recipient == '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1'
        assert transaction.associationType == 1
        assert transaction.txFee == 100000000


    def testSignWith(self):
        transaction = RevokeAssociation('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1, anchor='3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
        assert transaction.isSigned() is False
        transaction.signWith(self.account)
        assert transaction.isSigned() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.anchor == '3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj'
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.senderPublicKey == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verifySignature(transaction.toBinary(), transaction.proofs[0])

    def expectedV1(self):
        return ({
            "type": 17,
            "version": 1,
            "sender": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "hash": 'Hjh8aEYykDxvjksNKKM2SSun3nAmXvjg5cT8zqXubqrZPburn9qYebuJ5cFb',
            "associationType": 1,
            "recipient": '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
            "fee": 100000000,
            "timestamp": 1609773456000,
            "proofs": ['G7JKv9F6jPmSA6netZeSW5BKpmssmD6qLudRh1zt4Ce6T6cW8JBjqEmktyfaA7a6tLTrgdTPrDUwQdX8wMU1eah']
        })

    def expectedV3(self):
        return (
            {
                "type": 17,
                "version": 3,
                "sender": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
                "senderKeyType": "ed25519",
                "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
                "recipient": '3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1',
                "associationType": 1,
                "hash": 'Hjh8aEYykDxvjksNKKM2SSun3nAmXvjg5cT8zqXubqrZPburn9qYebuJ5cFb',
                "timestamp": 1609773456000,
                "fee": 100000000,
                "proofs": ['2kpKz4RUfThsoEKFutAJ9GzzFyMRzccWVKhwu3BS936YKBSB59Qn1xnLDVT449DgM9f3rXw6UTfPbuHGiTx3rmWc']
            }
        )

    def testToJson(self):
        transaction = RevokeAssociation('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1, '3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
        transaction.timestamp = 1609773456000
        transaction.signWith(self.account)
        if transaction.version == 1:
            expected = self.expectedV1()
        elif transaction.version == 3:
            expected = self.expectedV3()
        else:
            expected = ''

        assert transaction.toJson() == expected

    @mock.patch('LTO.PublicNode')
    def testBroadcast(self, mock_Class):
        transaction = RevokeAssociation('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1, '3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
        broadcastedTransaction = RevokeAssociation('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1', 1, '3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'

        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction

        assert mc.broadcast(transaction) == broadcastedTransaction


    def testFromData(self):
        data = {
            "type": 16,
            "version": 1,
            "recipient": "3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh",
            "associationType": 1,
            "hash": "3yMApqCuCjXDWPrbjfR5mjCPTHqFG8Pux1TxQrEM35jj",
            "id": "1uZqDjRjaehEceSxrVxz6WD6wt8su8TBHyDLQ1KFnJo",
            "sender": "3NBcx7AQqDopBj3WfwCVARNYuZyt1L9xEVM",
            "senderPublicKey": "7gghhSwKRvshZwwh6sG97mzo1qoFtHEQK7iM4vGcnEt7",
            "timestamp": 1610404930000,
            "fee": 100000000,
            "proofs": [
                "2jQMruoLoshfKe6FAUbA9vmVVvAt8bVpCFyM75Z2PLJiuRmjmLzFpM2UmgQ6E73qn46AVQprQJPBhQe92S7iSXbZ"
            ],
            "height": 1225712
        }
        transaction = RevokeAssociation(recipient='', associationType='').fromData(data)
        for key in data:
            assert data[key] == transaction.__getattr__(key)

