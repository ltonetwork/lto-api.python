from lto.public_node import PublicNode
from unittest import mock
from lto.accounts.ed25519.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from lto.transactions.transfer import Transfer
import pytest
import requests


class Resp:
    def __init__(self, code, text):
        self.status_code = code
        self.text = text

    def json(self):
        return {"code": self.status_code, "text": self.text}

    def raise_for_status(self):
        pass


# TODO Most of the tests that mock request, don't actually test anything
class TestPublicNode:
    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)
    node = PublicNode('https://tesnet.lto.network')

    def test_construct(self):
        node = PublicNode('https://nodes.lto.network')
        assert node.url == 'https://nodes.lto.network'

    @mock.patch.object(requests, 'get', return_value=Resp(300, '{ "message":"test"}'))
    def test_request(self, mocks):
        with pytest.raises(Exception):
            self.node.request('api')
        with mock.patch.object(requests, 'post', return_value=Resp(300, '{ "message":"test"}')):
            with pytest.raises(Exception):
                self.node.request(endpoint='/transactions/broadcast', post_data={"type": 4, "version": 2})

    @mock.patch.object(requests, 'get', return_value=Resp(200, 'test'))
    def test_request(self, mock):
        api = '/blocks/last'
        assert {'code': 200, 'text': 'test'} == self.node.request(api)

    def test_broadcast(self):
        transaction = Transfer('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', 10000000)
        with mock.patch.object(PublicNode, "request", return_value={
            'type': 4,
            'version': 3,
            'id': '74MeWagvnJ2MZTV7wEUQVWG8mTVddS9pJuqvtyG8b5eP',
            'sender': '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du',
            'senderKeyType': 'ed25519',
            'senderPublicKey': 'AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX',
            'fee': 100000000,
            'timestamp': 1631613596742,
            'recipient': '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj',
            'amount': 10000000,
            'attachment': '',
            'proofs': ['j2q6isq2atpXBADMZ2Vz7oRozfUKGuDkLnVMqtnXkwDhw6tyHmMMHTbaVknP4JmYiVWN5PuNp6i4f5TBhuc9QSm']
        }):
            response = PublicNode('https://tesnet.lto.network').broadcast(transaction)

        assert response.to_json() == {
            'type': 4,
            'version': 3,
            'sender': '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du',
            'senderKeyType': 'ed25519',
            'senderPublicKey': 'AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX',
            'fee': 100000000,
            'timestamp': 1631613596742,
            'amount': 10000000,
            'id': '74MeWagvnJ2MZTV7wEUQVWG8mTVddS9pJuqvtyG8b5eP',
            'recipient': '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj',
            'proofs': ['j2q6isq2atpXBADMZ2Vz7oRozfUKGuDkLnVMqtnXkwDhw6tyHmMMHTbaVknP4JmYiVWN5PuNp6i4f5TBhuc9QSm']
        }

    @mock.patch.object(PublicNode, 'request')
    def test_compile(self, mock):
        self.node.compile('sddsfdsf')
        mock.assert_called()

    @mock.patch.object(PublicNode, 'request')
    def test_height(self, mock):
        self.node.height()
        mock.assert_called()

    @mock.patch.object(PublicNode, 'request')
    def test_last_block(self, mock):
        self.node.last_block()
        mock.assert_called()

    @mock.patch.object(PublicNode, 'request')
    def test_block(self, mock):
        self.node.block(20)
        mock.assert_called()

    def test_balance(self):
        with mock.patch.object(PublicNode, "request", return_value={"balance": 5000_00000000}):
            balance = self.node.balance('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')
            assert balance == 5000_00000000

    def test_leasae_list(self):
        with mock.patch.object(PublicNode, "request"):
            self.node.lease_list('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')

    def test_sponsorship_list(self):
        with mock.patch.object(PublicNode, "request"):
            self.node.sponsorship_list('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')

    def test_transactions(self):
        with mock.patch.object(PublicNode, "request", return_value=1):
            self.node.transactions('3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')

    def test_tx(self):
        with mock.patch.object(PublicNode, 'request', return_value={
            'type': 4,
            'version': 3,
            'id': '74MeWagvnJ2MZTV7wEUQVWG8mTVddS9pJuqvtyG8b5eP',
            'sender': '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du',
            'senderKeyType': 'ed25519',
            'senderPublicKey': 'AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX',
            'fee': 100000000,
            'timestamp': 1631613596742,
            'recipient': '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj',
            'amount': 10000000,
            'attachment': '',
            'proofs': ['j2q6isq2atpXBADMZ2Vz7oRozfUKGuDkLnVMqtnXkwDhw6tyHmMMHTbaVknP4JmYiVWN5PuNp6i4f5TBhuc9QSm']
        }):
            response = self.node.tx('id')

        assert response.to_json() == {
            'id': '74MeWagvnJ2MZTV7wEUQVWG8mTVddS9pJuqvtyG8b5eP',
            'type': 4,
            'version': 3,
            'sender': '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du',
            'senderKeyType': 'ed25519',
            'senderPublicKey': 'AneNBwCMTG1YQ5ShPErzJZETTsHEWFnPWhdkKiHG6VTX',
            'fee': 100000000,
            'timestamp': 1631613596742,
            'amount': 10000000,
            'recipient': '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj',
            'proofs': ['j2q6isq2atpXBADMZ2Vz7oRozfUKGuDkLnVMqtnXkwDhw6tyHmMMHTbaVknP4JmYiVWN5PuNp6i4f5TBhuc9QSm']
        }
