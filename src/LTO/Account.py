import nacl.signing
from nacl.signing import VerifyKey
import ecdsa
from ecdsa import VerifyingKey

from LTO import crypto
import base58


class Account(object):

    SODIUM_CRYPTO_SIGN_BYTES = 64
    SODIUM_CRYPTO_SIGN_PUBLICKEYBYTES = 32

    def __init__(self, address, publicKey, privateKey = '', keyType='ed25519', seed='', nonce=0):
        self.address = address
        self.publicKey = publicKey
        self.privateKey = privateKey
        self.seed = seed
        self.nonce = nonce
        self.keyType = keyType

    def sign(self, message):
        if (self.privateKey == ''):
            raise Exception("Private key not set")
        if isinstance(self.privateKey, nacl.signing.SigningKey):
            return base58.b58encode(self.privateKey.sign(message).signature)
        elif isinstance(self.privateKey, ecdsa.SigningKey):
            return base58.b58encode(self.privateKey.sign(message))
        else:
            raise Exception('Encoding not supported')

    def getPublicKey(self):
        if isinstance(self.publicKey, VerifyKey):
            return base58.b58encode(bytes(self.publicKey))
        else:
            return base58.b58encode(self.publicKey.to_string(encoding="compressed"))

    def verifySignature(self, message: str, signature: str, encoding: str = 'base58'):
        if not self.publicKey:
            raise Exception('Unable to verify message; no public sign key')
        rawSignature = crypto.decode(signature, encoding)
        if isinstance(self.publicKey, VerifyKey):
            return self.publicKey.verify(message, rawSignature)
        elif isinstance(self.publicKey, VerifyingKey):
            print('ecdsa', base58.b58decode(signature))
            return self.publicKey.verify(rawSignature, message)
        else:
            raise Exception('Key type not supported')

    def getNetwork(self):
        return str(base58.b58decode(self.address))[6]
