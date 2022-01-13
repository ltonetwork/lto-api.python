import copy

from lto.accounts.account_factory import AccountFactory
from lto import crypto
import struct
from nacl.signing import SigningKey, VerifyKey
import base58
from lto.accounts.account import Account
from lto.accounts.ed25519.account_ed25519 import AccountED25519 as Account
from mnemonic import Mnemonic


class AccountFactoryED25519(AccountFactory):

    def __init__(self, chain_id, seed_method='brainwallet'):
        super().__init__(chain_id, seed_method)
        self.key_type = 'ed25519'
        self.mnemo = self.__create_mnemo(seed_method)

    def with_seed_method(self, seed_method):
        clone = super().with_seed_method(seed_method)
        if clone != self:
            self.mnemo = self.__create_mnemo(seed_method)

        return clone

    def create_sign_keys(self, seed, nonce=0):
        if self.seed_method == 'brainwallet':
            seed_hash = crypto.hash_chain(struct.pack(">L", nonce) + crypto.str2bytes(seed))
            account_seed_hash = crypto.sha256(seed_hash)
        elif self.seed_method == 'bip39' or self.seed_method.startswith('bip39:'):
            raise Exception('Seed method under construction')
            #account_seed_hash = self.mnemo.to_seed(seed)
        else:
            raise Exception('Unsupported seed method')
        private_key = SigningKey(account_seed_hash[:32])
        public_key = private_key.verify_key
        return private_key, public_key, self.key_type

    def create_address(self, public_key):
        unhashed_address = chr(1) + str(self.chain_id) + crypto.hash_chain(public_key.__bytes__())[0:20]
        address_hash = crypto.hash_chain(crypto.str2bytes(unhashed_address))[0:4]
        return base58.b58encode(crypto.str2bytes(unhashed_address + address_hash))

    def create_from_private_key(self, private_key):
        if not isinstance(private_key, SigningKey):
            public_key = VerifyKey(base58.b58decode(private_key)[-32:])
            private_key = SigningKey(seed=base58.b58decode(private_key)[:-32])
            address = self.create_address(public_key)
        else:
            public_key = private_key.verify_key
            address = self.create_address(public_key)
        return Account(address, public_key, private_key, self.key_type)

    def create_from_public_key(self, public_key):
        if isinstance(public_key, bytes):
            public_key = VerifyKey(public_key)
        elif isinstance(public_key, str):
            public_key = VerifyKey(base58.b58decode(public_key))

        if not isinstance(public_key, VerifyKey):
            raise Exception("Unrecognized Public Key format")

        address = self.create_address(public_key)

        return Account(address=address, public_key=public_key, key_type=self.key_type)

    def create_from_seed(self, seed, nonce=0):
        private_key, public_key, key_type = self.create_sign_keys(seed, nonce)
        address = self.create_address(public_key)
        return Account(address, public_key, private_key, key_type, seed, nonce)

    def create_with_values(self, address, public_key, private_key, key_type, seed=None):
        return Account(address, public_key, private_key, key_type, seed)

    def __create_mnemo(self, seed_method):
        if seed_method == 'bip39':
            return Mnemonic("english")
        elif seed_method.startswith('bip39:'):
            return Mnemonic(seed_method[6:])
        else:
            return None


