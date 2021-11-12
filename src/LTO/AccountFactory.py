import os
from LTO import crypto
from LTO.WordList import wordList
from abc import ABC, abstractmethod


class AccountFactory(ABC):

    def __init__(self, chainId):
        self.chainId = chainId

    @abstractmethod
    def createSignKeys(self, seed, nonce):
        pass

    @abstractmethod
    def createAddress(self, publicKey):
        pass

    def create(self):
        return self.createFromSeed(self.generateSeedPhrase())

    @abstractmethod
    def createFromSeed(self, seed, nonce=0):
        pass
        '''privateKey, publicKey, keyType = self.createSignKeys(seed, nonce)
        address = self.createAddress(publicKey)
        return Account(address, publicKey, privateKey, keyType, seed, nonce)'''

    @abstractmethod
    def createFromPrivateKey(self, privateKey):
        pass

    @abstractmethod
    def createFromPublicKey(self, publicKey):
        pass

    @abstractmethod
    def createWithValues(self, address, publicKey, privateKey, keyType, seed=''):
        pass

    @abstractmethod
    def assertAccount(self, account, address, publicKey, privateKey, keyType, seed):
        pass

    def generateSeedPhrase(self):
        wordCount = len(wordList)
        words = []
        for i in range(5):
            r = crypto.bytes2str(os.urandom(4))
            x = (ord(r[3])) + (ord(r[2]) << 8) + (ord(r[1]) << 16) + (ord(r[0]) << 24)
            w1 = x % wordCount
            w2 = ((int(x / wordCount) >> 0) + w1) % wordCount
            w3 = ((int((int(x / wordCount) >> 0) / wordCount) >> 0) + w2) % wordCount
            words.append(wordList[w1])
            words.append(wordList[w2])
            words.append(wordList[w3])
        return ' '.join(words)
