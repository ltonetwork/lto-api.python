from lto.accounts.account import Account
import base58
from lto import crypto


class AccountECDSA(Account):

    def init(self, address, public_key, private_key=None, key_type ='secp256k1',seed=None, nonce=0):
        super().__init__(address, public_key, private_key, key_type, seed, nonce)

    def get_public_key(self):
        return base58.b58encode(self.public_key.to_string(encoding="compressed"))

    def get_private_key(self):
        return base58.b58encode(self.private_key.to_string())

    def sign(self, message):
        if not self.private_key:
            raise Exception("Private key not set")
        return base58.b58encode(self.private_key.sign(message))

    def verify_signature(self, message: str, signature: str, encoding: str = 'base58'):
        if not self.public_key:
            raise Exception('Unable to verify message; no public sign key')
        raw_signature = crypto.decode(signature, encoding)
        return self.public_key.verify(raw_signature, message)
