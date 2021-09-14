import os
import struct

from nacl.signing import SigningKey
from nacl.signing import VerifyKey

from LTO.Account import Account
from LTO import crypto
from LTO.WordList import wordList

import base58


class AccountFactory(object):

    # this is the constructor
    def __init__(self, chainId):
        self.chainId = chainId

    def create(self):
        return self.createFromSeed(self.generateSeedPhrase())

    def createFromSeed(self, seed, nonce=0):
        privateKey, publicKey = self.createSignKeys(seed, nonce)
        address = self.createAddress(publicKey)
        return Account(address, publicKey, privateKey, seed)

    def createFromPrivateKey(self, privateKey):
        raise NotImplementedError

    def createFromPublicKey(self, publicKey):
        if not isinstance(publicKey, VerifyKey):
            decodedPublicKey = VerifyKey(base58.b58decode(publicKey))
            address = self.createAddress(decodedPublicKey)
        else:
            address = self.createAddress(publicKey)
        return Account(address, publicKey)

    def createWithValues(self, address, publicKey, privateKey, seed=''):
        return Account(address, publicKey, privateKey, seed)

    def assertAccount(self, account, address, publicKey, privateKey, seed):
        if address and account.address != address:
            return False
        if publicKey and account.publicKey != publicKey:
            return False
        if privateKey and account.privateKey != privateKey:
            return False
        return True

    # create the class from the seed
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

    # generate the private and public key from the seed
    def createSignKeys(self, seed, nonce=0):
        seedHash = crypto.hashChain(struct.pack(">L", nonce) + crypto.str2bytes(seed))
        accountSeedHash = crypto.sha256(seedHash)
        privateKey = SigningKey(accountSeedHash)
        publicKey = privateKey.verify_key
        return privateKey, publicKey

    def createAddress(self, publicKey):
        unhashedAddress = chr(1) + str(self.chainId) + crypto.hashChain(publicKey.__bytes__())[0:20]
        addressHash = crypto.hashChain(crypto.str2bytes(unhashedAddress))[0:4]
        return base58.b58encode(crypto.str2bytes(unhashedAddress + addressHash))
