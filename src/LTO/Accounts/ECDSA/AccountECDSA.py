from LTO.Account import Account
import base58
from LTO import crypto
import ecdsa

class AccountECDSA(Account):

    def init(self, address, publicKey, privateKey=None, keyType ='secp256k1',seed=None, nonce=0):
        super().__init__(address, publicKey, privateKey, keyType, seed, nonce)

    def getPublicKey(self):
        return base58.b58encode(self.publicKey.to_string(encoding="compressed"))

    def sign(self, message):
        if not self.privateKey:
            raise Exception("Private key not set")
        return base58.b58encode(self.privateKey.sign(message))

    def verifySignature(self, message: str, signature: str, encoding: str = 'base58'):
        if not self.publicKey:
            raise Exception('Unable to verify message; no public sign key')
        rawSignature = crypto.decode(signature, encoding)
        return self.publicKey.verify(rawSignature, message)
