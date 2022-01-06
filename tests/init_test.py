from unittest import mock
from lto import LTO
from lto.public_node import PublicNode
from lto.accounts.ed25519.account_ed25519 import AccountED25519 as Account

from lto.transactions.transfer import Transfer
from lto.transactions.anchor import Anchor
from lto.transactions.lease import Lease
from lto.transactions.association import Association
from lto.transactions.cancel_lease import CancelLease
from lto.transactions.cancel_sponsorship import CancelSponsorship
from lto.transactions.mass_transfer import MassTransfer
from lto.transactions.revoke_association import RevokeAssociation
from lto.transactions.set_script import SetScript
from lto.transactions.sponsorship import Sponsorship

import pytest


class TestInit():

    def testconstruct(self):
        pyclto = LTO()
        assert pyclto.NODE.url == PublicNode('https://testnet.lto.network').url
        assert pyclto.chain_id == 'T'
        pyclto = LTO('L')
        assert pyclto.NODE.url == PublicNode('https://nodes.lto.network').url
        assert pyclto.chain_id == 'L'
        pyclto = LTO('A')
        assert pyclto.NODE == ''

    def test_get_chain_id(self):
        pyclto = LTO()
        assert pyclto.getchain_id() == 'T'

    def test_account(self):
        pyclto = LTO()
        private_key = '4sEbCdhpYrZuYGsGSNCR9mJrZgLY6kTdFMGDZnK3oQtSCjyvMz3K6ZMo1GfGmbqHK95Pwx6WTi7vMLpFGbsgbfqz'
        seed = 'fragile because fox snap picnic mean art observe vicious program chicken purse text hidden chest'
        expectedAccount = Account(seed=seed, public_key='G3PaJt9cUvM5dVW8XAZnKrqmQj1xbSQ4yM7gWuknEKjn',
                                  private_key=private_key, address='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj')
        account = pyclto.Account(seed=seed)
        assert expectedAccount.address == account.address
        account = pyclto.Account(public_key='G3PaJt9cUvM5dVW8XAZnKrqmQj1xbSQ4yM7gWuknEKjn')
        assert expectedAccount.address == account.address
        assert pyclto.Account()

    def test_from_data(self):
        pyclto = LTO()
        data = ({
            "type": 4,
            "recipient": '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj',
            "amount": 100000000,
            "associationType": '',
            "anchor": '',
            "script": b'test'
        })
        with mock.patch.object(Transfer, "from_data"):
            pyclto.from_data(data)
        data['type'] = 16
        with mock.patch.object(Association, "from_data"):
            pyclto.from_data(data)
        data['type'] = 8
        with mock.patch.object(Lease, "from_data"):
            pyclto.from_data(data)
        data['type'] = 11
        with mock.patch.object(MassTransfer, "from_data"):
            pyclto.from_data(data)
        data['type'] = 15
        with mock.patch.object(Anchor, "from_data"):
            pyclto.from_data(data)
        data['type'] = 17
        with mock.patch.object(RevokeAssociation, "from_data"):
            pyclto.from_data(data)
        data['type'] = 18
        with mock.patch.object(Sponsorship, "from_data"):
            pyclto.from_data(data)
        data['type'] = 19
        with mock.patch.object(CancelSponsorship, "from_data"):
            pyclto.from_data(data)
        data['type'] = 9
        with mock.patch.object(CancelLease, "from_data"):
            pyclto.from_data(data)
        data['type'] = 13
        with pytest.raises(Exception):
            pyclto.from_data(data)
