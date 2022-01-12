import copy
from abc import ABC, abstractmethod
from lto.accounts.brainwallet import random_seed as brainwallet_random_seed
from lto.accounts.bip39 import random_seed as bip39_random_seed


class AccountFactory(ABC):
    def __init__(self, chain_id, seed_method):
        self.chain_id = chain_id
        self.seed_method = seed_method

    def with_seed_method(self, seed_method):
        if seed_method is None or self.seed_method == seed_method:
            return self

        clone = copy.copy(self)
        clone.seed_method = seed_method
        return clone

    @abstractmethod
    def create_sign_keys(self, seed, nonce):
        pass

    @abstractmethod
    def create_address(self, public_key):
        pass

    def create(self):
        if self.seed_method == 'brainwallet':
            seed = brainwallet_random_seed()
        else:
            raise Exception('Seed method under construction')

        '''elif self.seed_method == 'bip39':
            seed = bip39_random_seed()
        elif self.seed_method.startswith('bip39:'):
            # raise Exception("Method under construction")
            seed = bip39_random_seed(self.seed_method[6:])
        else:
            raise Exception('Unknown seed method')'''

        return self.create_from_seed(seed)

    @abstractmethod
    def create_from_seed(self, seed, nonce=0):
        pass

    @abstractmethod
    def create_from_private_key(self, private_key):
        pass

    @abstractmethod
    def create_from_public_key(self, public_key):
        pass

    @abstractmethod
    def create_with_values(self, address, public_key, private_key, key_type, seed=''):
        pass

