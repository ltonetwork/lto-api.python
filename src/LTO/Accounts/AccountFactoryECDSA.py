from LTO.AccountFactory import AccountFactory
from ecdsa import VerifyingKey, SECP256k1, NIST256p, SigningKey
from ecdsa.util import randrange_from_seed__trytryagain
import base58
from LTO import crypto
from LTO.Account import Account


class AccountECDSA(AccountFactory):

    def __init__(self, chainId, curve='secp256k1'):
        super().__init__(chainId)

        self.keyType = curve
        if curve == 'secp256k1':
            self.curve = SECP256k1
        elif curve == 'secp256r1':
            self.curve = NIST256p
        else:
            raise Exception("Curve not supported")

    def _MakeKey(self, seed):
        secexp = randrange_from_seed__trytryagain(seed, self.curve.order)
        return SigningKey.from_secret_exponent(secexp, curve=self.curve)

    def createSignKeys(self, seed, nonce=0):
        privateKey = self._MakeKey(seed)
        publicKey = privateKey.verifying_key
        return privateKey, publicKey, self.keyType

    def createAddress(self, publicKey):
        unhashedAddress = chr(1) + str(self.chainId) + crypto.hashChain(publicKey.to_string(encoding="compressed"))[0:20]
        addressHash = crypto.hashChain(crypto.str2bytes(unhashedAddress))[0:4]
        return base58.b58encode(crypto.str2bytes(unhashedAddress + addressHash))

    def createFromPublicKey(self, publicKey):
        if not isinstance(publicKey, VerifyingKey):
            if isinstance(publicKey, bytes):
                publicKey = VerifyingKey.from_string(publicKey, curve=self.curve)
            elif isinstance(publicKey, str):
                publicKey = base58.b58decode(publicKey)
                publicKey = VerifyingKey.from_string(publicKey, curve=self.curve)
            else:
                raise Exception("Unrecognized Public Key format")
        address = self.createAddress(publicKey)
        return Account(address=address, publicKey=publicKey, keyType=self.keyType)

    def createFromPrivateKey(self, privateKey):
        if not isinstance(privateKey, SigningKey):
            if isinstance(privateKey, bytes):
                privateKey = SigningKey.from_string(privateKey, curve=self.curve)
            elif isinstance(privateKey, str):
                privateKey = base58.b58decode(privateKey)
                privateKey = SigningKey.from_string(privateKey, curve=self.curve)
            else:
                raise Exception("Unrecognized Private Key format")
        publicKey = privateKey.verifying_key
        address = self.createAddress(publicKey)
        return Account(address=address, publicKey=publicKey, privateKey=privateKey, keyType=self.keyType)