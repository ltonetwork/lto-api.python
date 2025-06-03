from lto.accounts.account_factory import AccountFactory
from ecdsa import VerifyingKey, SECP256k1, NIST256p, SigningKey
import hashlib
from ecdsa.util import randrange_from_seed__trytryagain as randrange_from_seed
import base58
from lto import crypto
from lto.accounts.ecdsa.account_ecdsa import AccountECDSA as Account
from bip32 import BIP32
from mnemonic import Mnemonic

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

    def _make_key(self, seed):
        secexp = randrange_from_seed(seed, self.curve.order)
        return SigningKey.from_secret_exponent(secexp, curve=self.curve, hashfunc=hashlib.sha256)

    def create_sign_keys(self, seed, nonce=0):
        private_key = self._make_key(seed)
        public_key = private_key.verifying_key
        return private_key, public_key, self.key_type

    def create_address(self, public_key):
        unhashed_address = chr(1) + str(self.chain_id) + crypto.hash_chain(public_key.to_string(encoding="compressed"))[0:20]
        address_hash = crypto.hash_chain(crypto.str2bytes(unhashed_address))[0:4]
        return base58.b58encode(crypto.str2bytes(unhashed_address + address_hash))

    def create_from_public_key(self, public_key):
        if isinstance(public_key, VerifyingKey):
            return self._create_from_verifying_key(public_key)

        if isinstance(public_key, bytes):
            try:
                decoded = public_key.decode()
                public_key = decoded
            except UnicodeDecodeError:
                # Likely raw key bytes
                verifying_key = VerifyingKey.from_string(public_key, curve=self.curve, hashfunc=hashlib.sha256)
                return self._create_from_verifying_key(verifying_key)

        if isinstance(public_key, str):
            if "-----BEGIN" in public_key:
                verifying_key = VerifyingKey.from_pem(public_key)
                if verifying_key.curve != self.curve:
                    raise Exception(f"Curve mismatch: expected {self.curve.name}, got {verifying_key.curve.name}")
            else:
                try:
                    raw = base58.b58decode(public_key)
                except Exception:
                    raise Exception("Invalid base58 encoding")
                verifying_key = VerifyingKey.from_string(raw, curve=self.curve, hashfunc=hashlib.sha256)
        else:
            raise Exception("Unrecognized public key format")

        return self._create_from_verifying_key(verifying_key)

    def _create_from_verifying_key(self, public_key):
        address = self.create_address(public_key)
        return Account(address=address, public_key=public_key, key_type=self.key_type)

    def create_from_private_key(self, private_key):
        if isinstance(private_key, SigningKey):
            return self._create_from_signing_key(private_key)

        if isinstance(private_key, bytes):
            try:
                decoded = private_key.decode()
                private_key = decoded
            except UnicodeDecodeError:
                # Likely raw key bytes
                signing_key = SigningKey.from_string(private_key, curve=self.curve, hashfunc=hashlib.sha256)
                return self._create_from_signing_key(signing_key)

        if isinstance(private_key, str):
            if "-----BEGIN" in private_key:
                signing_key = SigningKey.from_pem(private_key)
                if signing_key.curve != self.curve:
                    raise Exception(f"Curve mismatch: expected {self.curve.name}, got {signing_key.curve.name}")
            else:
                raw = base58.b58decode(private_key)
                signing_key = SigningKey.from_string(raw, curve=self.curve, hashfunc=hashlib.sha256)
        else:
            raise Exception("Unrecognized private key format")

        return self._create_from_signing_key(signing_key)

    def _create_from_signing_key(self, private_key):
        public_key = private_key.verifying_key
        address = self.create_address(public_key)
        return Account(address=address, public_key=public_key, private_key=private_key, key_type=self.key_type)

    def create_from_seed(self, seed_phrase, nonce=0):
        mnemo = Mnemonic("english")
        seed = mnemo.to_seed(seed_phrase)
        bip32 = BIP32.from_seed(seed)

        path = f"m/44'/742'/0'/0/{nonce}"
        privkey_bytes = bip32.get_privkey_from_path(path)

        private_key = SigningKey.from_string(privkey_bytes, curve=self.curve, hashfunc=hashlib.sha256)
        public_key = private_key.verifying_key
        address = self.create_address(public_key)
        return Account(address, public_key, private_key, self.key_type, seed_phrase, nonce)

    def create(self):
        mnemo = Mnemonic("english")
        seed_phrase = mnemo.generate(strength=128)
        return self.create_from_seed(seed_phrase, 0)
