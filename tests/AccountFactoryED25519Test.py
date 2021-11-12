import base58
import unittest

from nacl.signing import VerifyKey

from LTO.Accounts.AccountFactoryED25519 import AccountFactoryED25519
from LTO.Account import Account
from LTO.tools import Tools


class AccountTest(unittest.TestCase):
    factory = AccountFactoryED25519('L')

    def testCreateAddress(self):
        expected = '3JmCa4jLVv7Yn2XkCnBUGsa7WNFVEMxAfWe'
        address = self.factory.createAddress(
            publicKey=VerifyKey(base58.b58decode("GjSacB6a5DFNEHjDSmn724QsrRStKYzkahPH67wyrhAY")))
        self.assertEqual(address, expected)

    def testCreateSignKeys(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        expectedPublic = '88Ny176gibcsKogkrkeR1MRJSpt9diaMdqnrnjLcy5PA'
        expectedPrivate = '8swwLhnY6CUYS9v4L8yANcpftsG52xqrmygHJ4saTdSp'
        privateKey, publicKey = self.factory.createSignKeys(seed)
        self.assertEqual(base58.b58encode(privateKey.__bytes__()), expectedPrivate)
        self.assertEqual(base58.b58encode(publicKey.__bytes__()), expectedPublic)

    def testCreateFromPublic(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        account = AccountFactoryED25519('T').createFromSeed(seed)
        account2 = AccountFactoryED25519('T').createFromPublicKey(account.publicKey)
        # object
        assert account.address == account2.address
        assert account.publicKey == account2.publicKey
        # bytes
        publicKey = b'i\xe5\xb5\xee\xa8\x01OT\xc6\xb1\x15\xec_\x97\xcf\xe9b\xb7\xab&\xe3\x1bN\xc4\xb5\xe2\xd4\x9f\xab!\x98e'
        account3 = AccountFactoryED25519('T').createFromPublicKey(base58.b58encode(publicKey))
        assert account.address == account3.address
        assert account.publicKey.__bytes__() == base58.b58decode(account3.publicKey)
        # b58 str
        account4 = AccountFactoryED25519('T').createFromPublicKey(base58.b58encode(publicKey))
        assert account.address == account4.address
        assert account.publicKey.__bytes__() == base58.b58decode(account4.publicKey)

    def testCreateFromSeed(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        publicKey = '88Ny176gibcsKogkrkeR1MRJSpt9diaMdqnrnjLcy5PA'
        privateKey = '8swwLhnY6CUYS9v4L8yANcpftsG52xqrmygHJ4saTdSp'
        address = '3JrXMae8BFDUrVu6DxuQTvvEVf8NwxdnPct'
        expectedAccount = Account(address=address, publicKey=VerifyKey(base58.b58decode(publicKey)),
                                    privateKey=VerifyKey(base58.b58decode(privateKey)), seed=seed)
        account = self.factory.createFromSeed(seed, nonce=0)
        assert account.address == address
        assert base58.b58encode(account.publicKey.__bytes__()) == publicKey
        assert base58.b58encode(account.privateKey.__bytes__()) == privateKey
        assert account.seed == account.seed

    def testAssertAccountTrue(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        publicKey = VerifyKey(base58.b58decode('88Ny176gibcsKogkrkeR1MRJSpt9diaMdqnrnjLcy5PA'))
        privateKey = VerifyKey(base58.b58decode('8swwLhnY6CUYS9v4L8yANcpftsG52xqrmygHJ4saTdSp'))
        address = '3JrXMae8BFDUrVu6DxuQTvvEVf8NwxdnPct'
        account = Account(address=address, publicKey=publicKey, privateKey=privateKey, seed=seed)

    def testAssertAccountFalse(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        publicKey = VerifyKey(base58.b58decode('88Ny176gibcsKogkrkeR1MRJSpt9diaMdqnrnjLcy5PA'))
        privateKey = VerifyKey(base58.b58decode('8swwLhnY6CUYS9v4L8yANcpftsG52xqrmygHJ4saTdSp'))
        address = '3JrXMae8BFDUrVu6DxuQTvvEVf8NwxdnPct'
        account = Account(address='5JrXMae9BFDUrVu6DxuQTvvEVf8NwxdnPct', publicKey=publicKey, privateKey=privateKey, seed=seed)

    def testGenerateSeedPhrase(self):
        seedPhrase = self.factory.generateSeedPhrase()
        self.assertIs(15, len(seedPhrase.split()))

    def testCreateFromPrivateKey(self):
        seed = 'fragile because fox snap picnic mean art observe vicious program chicken purse text hidden chest'
        account = AccountFactoryED25519('T').createFromSeed(seed)
        account2 = AccountFactoryED25519('T').createFromPrivateKey(account.privateKey)
        assert account.address == account2.address
        assert account.publicKey == account2.publicKey
        assert account.privateKey == account2.privateKey

        privateKey = '4sEbCdhpYrZuYGsGSNCR9mJrZgLY6kTdFMGDZnK3oQtSCjyvMz3K6ZMo1GfGmbqHK95Pwx6WTi7vMLpFGbsgbfqz'
        account3 = AccountFactoryED25519('T').createFromPrivateKey(privateKey)
        assert account.address == account3.address
        assert account.publicKey == account3.publicKey
        assert account.privateKey.__bytes__() == account3.privateKey

