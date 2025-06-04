from lto import crypto
from abc import ABC, abstractmethod


class Account(ABC):

    def __init__(self, address, public_key, private_key=None, key_type='ed25519', seed=None, nonce=0):
        self.address = address
        self.public_key = public_key
        self.private_key = private_key
        self.seed = seed
        self.nonce = nonce
        self.key_type = key_type

    @abstractmethod
    def get_public_key(self):
        pass

    @abstractmethod
    def sign(self, message):
        pass

    @abstractmethod
    def verify(self, message: str, signature: str, encoding: str = 'base58'):
        pass

    # Deprecated: use verify instead
    def verify_signature(self, message: str, signature: str, encoding: str = 'base58'):
        return self.verify(message, signature, encoding=encoding)

    def get_network(self):
        return crypto.get_network(self.address)
