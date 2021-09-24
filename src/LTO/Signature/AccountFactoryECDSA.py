from LTO.AccountFactory import AccountFactory
from ecdsa import VerifyingKey, SECP256k1, SigningKey
from ecdsa.util import randrange_from_seed__trytryagain
import base58
from LTO import crypto
from LTO.Account import Account


class AccountECDSA(AccountFactory):

    def __init__(self, chainId):
        super().__init__()
        self.chainId = chainId

    def make_key(self, seed):
        secexp = randrange_from_seed__trytryagain(seed, SECP256k1.order)
        return SigningKey.from_secret_exponent(secexp, curve=SECP256k1)

    def createSignKeys(self, seed, nonce=0):
        privateKey = self.make_key(seed)
        publicKey = privateKey.verifying_key
        return privateKey, publicKey

    def createAddress(self, publicKey):
        unhashedAddress = chr(1) + str(self.chainId) + crypto.hashChain(publicKey.to_string())[0:20]
        addressHash = crypto.hashChain(crypto.str2bytes(unhashedAddress))[0:4]
        return base58.b58encode(crypto.str2bytes(unhashedAddress + addressHash))

    def createFromPublicKey(self, publicKey):
        if not isinstance(publicKey, VerifyingKey):
            publicKey = VerifyingKey.from_string(publicKey, curve=SECP256k1)
        address = self.createAddress(publicKey)
        return Account(address=address, publicKey=publicKey)

    def createFromPrivateKey(self, privateKey):
        if not isinstance(privateKey, SigningKey):
            privateKey = SigningKey.from_string(privateKey, curve=SECP256k1)
        publicKey = privateKey.verifying_key
        address = self.createAddress(publicKey)
        return Account(address=address, publicKey=publicKey, privateKey=privateKey)