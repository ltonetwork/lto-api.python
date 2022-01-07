import os
from lto import crypto
from lto.word_list import wordList
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

    def create(self):
        return self.create_from_seed(self.generate_seed())

    @abstractmethod
    def create_from_seed(self, seed, nonce=0):
        pass
        '''private_key, public_key, key_type = self.create_sign_keys(seed, nonce)
        address = self.create_address(public_key)
        return Account(address, public_key, private_key, key_type, seed, nonce)'''

    @abstractmethod
    def create_from_private_key(self, private_key):
        pass

    @abstractmethod
    def create_from_public_key(self, public_key):
        pass

    @abstractmethod
    def create_with_values(self, address, public_key, private_key, key_type, seed=''):
        pass

    def generate_seed(self):
        word_count = len(wordList)
        words = []
        for i in range(5):
            r = crypto.bytes2str(os.urandom(4))
            x = (ord(r[3])) + (ord(r[2]) << 8) + (ord(r[1]) << 16) + (ord(r[0]) << 24)
            w1 = x % word_count
            w2 = ((int(x / word_count) >> 0) + w1) % word_count
            w3 = ((int((int(x / word_count) >> 0) / word_count) >> 0) + w2) % word_count
            words.append(wordList[w1])
            words.append(wordList[w2])
            words.append(wordList[w3])
        return ' '.join(words)
