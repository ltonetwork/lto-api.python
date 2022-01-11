from __future__ import absolute_import, division, print_function, unicode_literals

import base58

from lto.accounts import AccountFactory
from lto.public_node import PublicNode
from lto.accounts import AccountFactoryECDSA, AccountFactoryED25519


class LTO:

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

    def Account(self, public_key=None, private_key=None, key_type='ed25519', seed=None, seed_method=None, nonce=0):
        factory = self.account_factories[key_type].with_seed_method(seed_method)

        if seed:
            account = factory.create_from_seed(seed, nonce)
        elif private_key:
            account = factory.create_from_private_key(private_key)
        elif public_key:
            account = factory.create_from_public_key(public_key)
        else:
            account = factory.create()

        # assert public_key is None or account.get_public_key() == self.__key_base58(public_key), "Public key mismatch"
        # assert private_key is None or account.get_private_key() == self.__key_base58(private_key), "Private key mismatch"

        return account

    @staticmethod
    def __key_base58(key):
        if type(key) == object:
            return base58.b58encode(bytes(key))
        elif type(key) == bytes:
            return base58.b58encode(key)
        else:
            return key
