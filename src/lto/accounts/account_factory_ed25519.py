from lto.account_factory import AccountFactory
from lto import crypto
import struct
from nacl.signing import SigningKey, VerifyKey
import base58
from lto.account import Account
from lto.accounts.ed25519.account_ed25519 import AccountED25519 as Account
# from lto.accounts.ed25519 import SigningKeyED25519 as SigningKey


class AccountFactoryED25519(AccountFactory):

    def __init__(self, chain_id):
        super().__init__(chain_id)
        self.key_type = 'ed25519'

    def create_sign_keys(self, seed, nonce=0):
        seed_hash = crypto.hash_chain(struct.pack(">L", nonce) + crypto.str2bytes(seed))
        account_seed_hash = crypto.sha256(seed_hash)
        private_key = SigningKey(account_seed_hash)
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

