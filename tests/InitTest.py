from unittest import mock
from LTO import PyCLTO
from LTO.PublicNode import PublicNode
from LTO.Account import Account

from LTO.Transactions.Transfer import Transfer
from LTO.Transactions.Anchor import Anchor
from LTO.Transactions.Lease import Lease
from LTO.Transactions.Association import Association
from LTO.Transactions.CancelLease import CancelLease
from LTO.Transactions.CancelSponsorship import CancelSponsorship
from LTO.Transactions.MassTransfer import MassTransfer
from LTO.Transactions.RevokeAssociation import RevokeAssociation
from LTO.Transactions.SetScript import SetScript
from LTO.Transactions.Sponsorship import Sponsorship

import pytest

class TestInit():

    def testconstruct(self):
        pyclto = PyCLTO()
        assert pyclto.NODE.url == PublicNode('https://testnet.lto.network').url
        assert pyclto.chainId == 'T'
        pyclto = PyCLTO('L')
        assert pyclto.NODE.url == PublicNode('https://nodes.lto.network').url
        assert pyclto.chainId == 'L'
        pyclto = PyCLTO('A')
        assert pyclto.NODE == ''

    def testGetChainId(self):
        pyclto = PyCLTO()
        assert pyclto.getChainId() == 'T'

    def testAccount(self):
        pyclto = PyCLTO()
        privatekey = '4sEbCdhpYrZuYGsGSNCR9mJrZgLY6kTdFMGDZnK3oQtSCjyvMz3K6ZMo1GfGmbqHK95Pwx6WTi7vMLpFGbsgbfqz'
        seed = 'fragile because fox snap picnic mean art observe vicious program chicken purse text hidden chest'
        expectedAccount = Account(seed=seed, publicKey='G3PaJt9cUvM5dVW8XAZnKrqmQj1xbSQ4yM7gWuknEKjn', privateKey=privatekey, address='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')
        account = pyclto.Account(seed=seed)
        assert expectedAccount.address == account.address
        account = pyclto.Account(publicKey='G3PaJt9cUvM5dVW8XAZnKrqmQj1xbSQ4yM7gWuknEKjn')
        assert expectedAccount.address == account.address
        with pytest.raises(Exception):
            pyclto.Account(privateKey=privatekey)
        assert pyclto.Account()




    def testFromData(self):
        pyclto = PyCLTO()
        data = ({
            "type": 4,
            "recipient": '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj',
            "amount": 100000000,
            "associationType":'',
            "anchor":'',
            "script": b'test'
        })
        with mock.patch.object(Transfer, "fromData"):
            pyclto.fromData(data)
        data['type'] = 16
        with mock.patch.object(Association, "fromData"):
            pyclto.fromData(data)
        data['type'] = 8
        with mock.patch.object(Lease, "fromData"):
            pyclto.fromData(data)
        data['type'] = 11
        with mock.patch.object(MassTransfer, "fromData"):
            pyclto.fromData(data)
        data['type'] = 15
        with mock.patch.object(Anchor, "fromData"):
            pyclto.fromData(data)
        data['type'] = 17
        with mock.patch.object(RevokeAssociation, "fromData"):
            pyclto.fromData(data)
        data['type'] = 18
        with mock.patch.object(Sponsorship, "fromData"):
            pyclto.fromData(data)
        data['type'] = 19
        with mock.patch.object(CancelSponsorship, "fromData"):
            pyclto.fromData(data)
        data['type'] = 9
        with mock.patch.object(CancelLease, "fromData"):
            pyclto.fromData(data)
        data['type'] = 13
        with mock.patch.object(SetScript, "fromData"):
            pyclto.fromData(data)
        data['type'] = 0
        with pytest.raises(Exception):
            pyclto.fromData(data)


