from LTO.Account import Account
import base58
from LTO import crypto
from nacl.signing import SigningKey, VerifyKey


class AccountED25519(Account):

    def init(self, address, publicKey, privateKey=None, seed=None, nonce=0):
        super().__init__(address, publicKey, privateKey, 'ed25519', seed, nonce)


    def getPublicKey(self):
        return base58.b58encode(bytes(self.publicKey))

    def sign(self, message):
        if not self.privateKey:
            raise Exception("Private key not set")
        return base58.b58encode(self.privateKey.sign(message).signature)

    def verifySignature(self, message: str, signature: str, encoding: str = 'base58'):
        if not self.publicKey:
            raise Exception('Unable to verify message; no public sign key')
        rawSignature = crypto.decode(signature, encoding)
        return self.publicKey.verify(message, rawSignature)


