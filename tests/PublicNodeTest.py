from LTO.PublicNode import PublicNode
from unittest import mock
from Transactions.Transfer import Transfer
from LTO.AccountFactory import AccountFactory

class TestPublicNode:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)
    node = PublicNode('https://tesnet.lto.network')

    def testConstruct(self):
        node = PublicNode('https://nodes.lto.network')
        assert node.url == 'https://nodes.lto.network'



    @mock.patch('LTO.PublicNode')
    def testWrapper(self, mock_Class):
        api = '/transactions/broadcast'
        postData = {"type": 4, "version": 2, "sender": "3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du", "senderPublicKey": "AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX", "fee": 100000000, "timestamp": 1631613596742, "amount": 10000000, "recipient": "3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj", "attachment": "", "proofs": ["j2q6isq2atpXBADMZ2Vz7oRozfUKGuDkLnVMqtnXkwDhw6tyHmMMHTbaVknP4JmYiVWN5PuNp6i4f5TBhuc9QSm"]}
        mc = mock_Class.return_value
        mc.wrapper.return_value = {'type': 4, 'version': 2, 'id': '74MeWagvnJ2MZTV7wEUQVWG8mTVddS9pJuqvtyG8b5eP', 'sender': '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du', 'senderKeyType': 'ed25519', 'senderPublicKey': 'AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX', 'fee': 100000000, 'timestamp': 1631613596742, 'recipient': '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', 'amount': 10000000, 'attachment': '', 'proofs': ['j2q6isq2atpXBADMZ2Vz7oRozfUKGuDkLnVMqtnXkwDhw6tyHmMMHTbaVknP4JmYiVWN5PuNp6i4f5TBhuc9QSm']}
        assert mc.wrapper(api, postData) == {'type': 4, 'version': 2, 'id': '74MeWagvnJ2MZTV7wEUQVWG8mTVddS9pJuqvtyG8b5eP', 'sender': '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du', 'senderKeyType': 'ed25519', 'senderPublicKey': 'AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX', 'fee': 100000000, 'timestamp': 1631613596742, 'recipient': '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', 'amount': 10000000, 'attachment': '', 'proofs': ['j2q6isq2atpXBADMZ2Vz7oRozfUKGuDkLnVMqtnXkwDhw6tyHmMMHTbaVknP4JmYiVWN5PuNp6i4f5TBhuc9QSm']}

'''    @mock.patch('LTO.PublicNode')
    def testBroadcast(self, mock_Class):
        transaction = Transfer('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', 10000000)
        transaction.signWith(self.account)
        mc = mock_Class.return_value
        mc.wrapper.return_value = {'type': 4, 'version': 2, 'id': '74MeWagvnJ2MZTV7wEUQVWG8mTVddS9pJuqvtyG8b5eP', 'sender': '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du', 'senderKeyType': 'ed25519', 'senderPublicKey': 'AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX', 'fee': 100000000, 'timestamp': 1631613596742, 'recipient': '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', 'amount': 10000000, 'attachment': '', 'proofs': ['j2q6isq2atpXBADMZ2Vz7oRozfUKGuDkLnVMqtnXkwDhw6tyHmMMHTbaVknP4JmYiVWN5PuNp6i4f5TBhuc9QSm']}
        response = self.node.broadcast(transaction)
        assert response.toJson() == {'type': 4, 'version': 2, 'sender': '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du', 'senderPublicKey': 'AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX', 'fee': 100000000, 'timestamp': 1631613596742, 'amount': 10000000, 'recipient': '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', 'attachment': '', 'proofs': ['j2q6isq2atpXBADMZ2Vz7oRozfUKGuDkLnVMqtnXkwDhw6tyHmMMHTbaVknP4JmYiVWN5PuNp6i4f5TBhuc9QSm']}
'''
