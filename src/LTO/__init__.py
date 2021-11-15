from __future__ import absolute_import, division, print_function, unicode_literals

from LTO.account_factory import AccountFactory
from LTO.public_node import PublicNode

from LTO.Transactions.anchor import Anchor
from LTO.Transactions.lease import Lease
from LTO.Transactions.association import Association
from LTO.Transactions.cancel_lease import CancelLease
from LTO.Transactions.cancel_sponsorship import CancelSponsorship
from LTO.Transactions.mass_transfer import MassTransfer
from LTO.Transactions.revoke_association import RevokeAssociation
from LTO.Transactions.set_script import SetScript
from LTO.Transactions.sponsorship import Sponsorship
from LTO.Transactions.transfer import Transfer
from LTO.Accounts.account_factory_ecdsa import AccountFactoryECDSA
from LTO.Accounts.account_factory_ed25519 import AccountFactoryED25519


class PyCLTO:

    def __init__(self, chain_id='T'):

        if chain_id == 'T':
            self.NODE = PublicNode('https://testnet.lto.network')
        elif chain_id == 'L':
            self.NODE = PublicNode('https://nodes.lto.network')
        else:
            self.NODE = ''

        self.chain_id = chain_id

        self.account_factories = {
            'ed25519': AccountFactoryED25519(chain_id),
            'secp256r1': AccountFactoryECDSA(chain_id, curve='secp256r1'),
            'secp256k1': AccountFactoryECDSA(chain_id, curve='secp256k1')
        }

    def Account(self, public_key=None, private_key=None, key_type='ed25519', seed=None, nonce=0):
        factory = self.account_factories[key_type]
        if seed:
            account = factory.create_from_seed(seed, nonce)
        elif private_key:
            account = factory.create_from_private_key(private_key)
        elif public_key:
            account = factory.create_from_public_key(public_key)
        else:
            account = factory.create()
        return account

    def getchain_id(self):
        return self.chain_id

    def from_data(self, data):

        if data['type'] == 4:
            return Transfer(recipient=data['recipient'], amount=data['amount']).from_data(data)
        elif data['type'] == 8:
            return Lease(amount=1, recipient='').from_data(data)
        elif data['type'] == 11:
            return MassTransfer(transfers='').from_data(data)
        elif data['type'] == 15:
            return Anchor(anchor='').from_data(data)
        elif data['type'] == 16:
            return Association(recipient='', association_type='', anchor='').from_data(data)
        elif data['type'] == 17:
            return RevokeAssociation(recipient='', association_type='').from_data(data)
        elif data['type'] == 18:
            return Sponsorship(data['recipient']).from_data(data)
        elif data['type'] == 19:
            return CancelSponsorship(data['recipient']).from_data(data)
        elif data['type'] == 13:
            return SetScript(data['script']).from_data(data)
        elif data['type'] == 9:
            return CancelLease(leaseId='').from_data(data)
        else:
            raise Exception('Incorrect transaction Type')
