from lto.account_factory import AccountFactory
from ecdsa import VerifyingKey, SECP256k1, NIST256p, SigningKey
import hashlib
from ecdsa.util import randrange_from_seed__trytryagain
import base58
from lto import crypto
from lto.accounts.ecdsa.account_ecdsa import AccountECDSA as Account


class AccountFactoryECDSA(AccountFactory):

    def __init__(self, chain_id, curve='secp256k1'):
        super().__init__(chain_id)

        self.key_type = curve
        if curve == 'secp256k1':
            self.curve = SECP256k1
        elif curve == 'secp256r1':
            self.curve = NIST256p
        else:
            raise Exception("Curve not supported")

    def _MakeKey(self, seed):
        secexp = randrange_from_seed__trytryagain(seed, self.curve.order)
        return SigningKey.from_secret_exponent(secexp, curve=self.curve, hashfunc=hashlib.sha256)

    def create_sign_keys(self, seed, nonce=0):
        private_key = self._MakeKey(seed)
        public_key = private_key.verifying_key
        return private_key, public_key, self.key_type

    def create_address(self, public_key):
        unhashed_address = chr(1) + str(self.chain_id) + crypto.hash_chain(public_key.to_string(encoding="compressed"))[0:20]
        address_hash = crypto.hash_chain(crypto.str2bytes(unhashed_address))[0:4]
        return base58.b58encode(crypto.str2bytes(unhashed_address + address_hash))

    def create_from_public_key(self, public_key):
        if not isinstance(public_key, VerifyingKey):
            if isinstance(public_key, bytes):
                public_key = VerifyingKey.from_string(public_key, curve=self.curve, hashfunc=hashlib.sha256)
            elif isinstance(public_key, str):
                public_key = base58.b58decode(public_key)
                public_key = VerifyingKey.from_string(public_key, curve=self.curve, hashfunc=hashlib.sha256)
            else:
                raise Exception("Unrecognized Public Key format")
        address = self.create_address(public_key)
        return Account(address=address, public_key=public_key, key_type=self.key_type)

    def create_from_private_key(self, private_key):
        if not isinstance(private_key, SigningKey):
            if isinstance(private_key, bytes):
                private_key = SigningKey.from_string(private_key, curve=self.curve, hashfunc=hashlib.sha256)
            elif isinstance(private_key, str):
                private_key = base58.b58decode(private_key)
                private_key = SigningKey.from_string(private_key, curve=self.curve, hashfunc=hashlib.sha256)
            else:
                raise Exception("Unrecognized Private Key format")
        public_key = private_key.verifying_key
        address = self.create_address(public_key)
        return Account(address=address, public_key=public_key, private_key=private_key, key_type=self.key_type)

    def create_from_seed(self, seed, nonce=0):
        private_key, public_key, key_type = self.create_sign_keys(seed, nonce)
        address = self.create_address(public_key)
        return Account(address, public_key, private_key, key_type, seed, nonce)

    def create_with_values(self, address, public_key, private_key, key_type, seed=None):
        return Account(address, public_key, private_key, key_type, seed)
