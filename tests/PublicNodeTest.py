from LTO.PublicNode import PublicNode
from unittest import mock
from LTO.Accounts.AccountFactoryED25519 import AccountED25519 as AccountFactory
from LTO.Transactions.Transfer import Transfer
import pytest
import requests

class resp():
    def __init__(self, code, text):
        self.status_code = code
        self.text = text

    def json(self):
        return ({"code": self.status_code,
                 "text": self.text})

    def raise_for_status(self):
        pass

class TestPublicNode:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)
    node = PublicNode('https://tesnet.lto.network')

    def testConstruct(self):
        node = PublicNode('https://nodes.lto.network')
        assert node.url == 'https://nodes.lto.network'

    @mock.patch.object(requests, 'get', return_value=resp(300, '{ "message":"test"}'))
    def testWrapper(self, mocks):
        with pytest.raises(Exception):
            self.node.wrapper('api')
        with mock.patch.object(requests, 'post', return_value=resp(300, '{ "message":"test"}')):
            with pytest.raises(Exception):
                self.node.wrapper(api='/transactions/broadcast', postData={"type": 4, "version": 2})

    @mock.patch.object(requests, 'get', return_value=resp(200, 'test'))
    def testWrapper2(self, mock):
        api = '/blocks/last'
        assert {'code': 200, 'text': 'test'} == self.node.wrapper(api)


    def testBroadcast(self):
        transaction = Transfer('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', 10000000)
        with mock.patch.object(PublicNode, "wrapper", return_value={'type': 4, 'version': 3, 'id': '74MeWagvnJ2MZTV7wEUQVWG8mTVddS9pJuqvtyG8b5eP', 'sender': '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du', 'senderKeyType': 'ed25519', 'senderPublicKey': 'AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX', 'fee': 100000000, 'timestamp': 1631613596742, 'recipient': '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', 'amount': 10000000, 'attachment': '', 'proofs': ['j2q6isq2atpXBADMZ2Vz7oRozfUKGuDkLnVMqtnXkwDhw6tyHmMMHTbaVknP4JmYiVWN5PuNp6i4f5TBhuc9QSm']}):
            response = PublicNode('https://tesnet.lto.network').broadcast(transaction)
        assert response.toJson() == {
            'type': 4, 'version': 3, 'sender': '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du',
            'senderKeyType': 'ed25519',
            'senderPublicKey': 'AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX',
            'fee': 100000000, 'timestamp': 1631613596742, 'amount': 10000000,
            'recipient': '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', 'attachment': '', 'proofs': [
            'j2q6isq2atpXBADMZ2Vz7oRozfUKGuDkLnVMqtnXkwDhw6tyHmMMHTbaVknP4JmYiVWN5PuNp6i4f5TBhuc9QSm']}

    @mock.patch.object(PublicNode, 'wrapper')
    def testGetScript(self, mock):
        self.node.getScript('sddsfdsf')
        mock.assert_called()

    @mock.patch.object(PublicNode, 'wrapper')
    def testHeight(self, mock):
        self.node.height()
        mock.assert_called()

    @mock.patch.object(PublicNode, 'wrapper')
    def testLastBlock(self, mock):
        self.node.lastblock()
        mock.assert_called()

    @mock.patch.object(PublicNode, 'wrapper')
    def testBlock(self, mock):
        self.node.block(20)
        mock.assert_called()

    def testBalance(self):
        with mock.patch.object(PublicNode, "wrapper", return_value=1):
            self.node.balance('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')
        with pytest.raises(Exception):
            self.node.balance()

    def testLeasaeList(self):
        with mock.patch.object(PublicNode, "wrapper"):
            self.node.leaseList('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')
        with pytest.raises(Exception):
            self.node.leaseList()

    def testSponsorshipList(self):
        with mock.patch.object(PublicNode, "wrapper"):
            self.node.sponsorshipList('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')
        with pytest.raises(Exception):
            self.node.sponsorshipList()

    def testTransaction(self):
        with mock.patch.object(PublicNode, "wrapper", return_value=1):
            self.node.transactions()

    @mock.patch.object(PublicNode, 'wrapper', return_value={'type': 4, 'version': 3, 'id': '74MeWagvnJ2MZTV7wEUQVWG8mTVddS9pJuqvtyG8b5eP', 'sender': '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du', 'senderKeyType': 'ed25519', 'senderPublicKey': 'AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX', 'fee': 100000000, 'timestamp': 1631613596742, 'recipient': '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', 'amount': 10000000, 'attachment': '', 'proofs': ['j2q6isq2atpXBADMZ2Vz7oRozfUKGuDkLnVMqtnXkwDhw6tyHmMMHTbaVknP4JmYiVWN5PuNp6i4f5TBhuc9QSm']})
    def testTx(self, mock):
        response = self.node.tx('id')
        mock.assert_called()
        assert response.toJson() == {
            'type': 4, 'version': 3, 'sender': '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du',
            'senderKeyType': 'ed25519',
            'senderPublicKey': 'AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX',
            'fee': 100000000, 'timestamp': 1631613596742, 'amount': 10000000,
            'recipient': '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', 'attachment': '', 'proofs': [
                'j2q6isq2atpXBADMZ2Vz7oRozfUKGuDkLnVMqtnXkwDhw6tyHmMMHTbaVknP4JmYiVWN5PuNp6i4f5TBhuc9QSm']}




