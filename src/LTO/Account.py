from LTO import crypto
from abc import ABC, abstractmethod


class Account(ABC):

    def __init__(self, address, publicKey, privateKey=None, keyType='ed25519', seed=None, nonce=0):
        self.address = address
        self.publicKey = publicKey
        self.privateKey = privateKey
        self.seed = seed
        self.nonce = nonce
        self.keyType = keyType

    @abstractmethod
    def getPublicKey(self):
        pass

    @abstractmethod
    def sign(self, message):
        pass

    @abstractmethod
    def verifySignature(self, message: str, signature: str, encoding: str = 'base58'):
        pass

    def getNetwork(self):
        return crypto.getNetwork(self.address)
