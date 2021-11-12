from LTO.AccountFactory import AccountFactory
from LTO import crypto
import struct
from nacl.signing import SigningKey, VerifyKey
import base58
from LTO.Account import Account
from LTO.Accounts.ED25519.AccountED25519 import AccountED25519 as Account
# from LTO.Accounts.ED25519 import SigningKeyED25519 as SigningKey


class AccountFactoryED25519(AccountFactory):

    def __init__(self, chainId):
        super().__init__(chainId)
        self.keyType = 'ed25519'

    def createSignKeys(self, seed, nonce=0):
        seedHash = crypto.hashChain(struct.pack(">L", nonce) + crypto.str2bytes(seed))
        accountSeedHash = crypto.sha256(seedHash)
        privateKey = SigningKey(accountSeedHash)
        publicKey = privateKey.verify_key
        return privateKey, publicKey, self.keyType

    def createAddress(self, publicKey):
        unhashedAddress = chr(1) + str(self.chainId) + crypto.hashChain(publicKey.__bytes__())[0:20]
        addressHash = crypto.hashChain(crypto.str2bytes(unhashedAddress))[0:4]
        return base58.b58encode(crypto.str2bytes(unhashedAddress + addressHash))

    def createFromPrivateKey(self, privateKey):
        if not isinstance(privateKey, SigningKey):
            publicKey = VerifyKey(base58.b58decode(privateKey)[-32:])
            privateKey = SigningKey(seed=base58.b58decode(privateKey)[:-32])
            address = self.createAddress(publicKey)
        else:
            publicKey = privateKey.verify_key
            address = self.createAddress(publicKey)
        return Account(address, publicKey, privateKey, self.keyType)

    def createFromPublicKey(self, publicKey):
        if isinstance(publicKey, bytes):
            publicKey = VerifyKey(publicKey)
        elif isinstance(publicKey, str):
            publicKey = VerifyKey(base58.b58decode(publicKey))

        if not isinstance(publicKey, VerifyKey):
            raise Exception("Unrecognized Public Key format")

        address = self.createAddress(publicKey)

        return Account(address=address, publicKey=publicKey, keyType=self.keyType)

    def createFromSeed(self, seed, nonce=0):
        privateKey, publicKey, keyType = self.createSignKeys(seed, nonce)
        address = self.createAddress(publicKey)
        return Account(address, publicKey, privateKey, keyType, seed, nonce)

    def createWithValues(self, address, publicKey, privateKey, keyType, seed=None):
        return Account(address, publicKey, privateKey, keyType, seed)

