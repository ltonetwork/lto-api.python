from abc import ABC, abstractmethod

class AccountFactory(ABC):
    def __init__(self, chain_id):
        self.chain_id = chain_id

    @abstractmethod
    def create_sign_keys(self, seed, nonce):
        pass

    @abstractmethod
    def create_address(self, public_key):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def create_from_seed(self, seed, nonce=0):
        pass

    @abstractmethod
    def create_from_private_key(self, private_key):
        pass

    @abstractmethod
    def create_from_public_key(self, public_key):
        pass
