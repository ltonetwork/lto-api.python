import base58
import unittest

from nacl.signing import VerifyKey

import AccountFactory
import Account
import Tools


class AccountTest(unittest.TestCase):
    factory = AccountFactory('L')

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
        publicKey = '88Ny176gibcsKogkrkeR1MRJSpt9diaMdqnrnjLcy5PA'
        expectedAddress = '3JrXMae8BFDUrVu6DxuQTvvEVf8NwxdnPct'
        expectedAccount = Account(address=expectedAddress, publicKey=VerifyKey(base58.b58decode(publicKey)))
        account = self.factory.createFromPublicKey(VerifyKey(base58.b58decode(publicKey)))
        Tools().__eq__(expectedAccount, account)

    def testCreateFromSeed(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        publicKey = '88Ny176gibcsKogkrkeR1MRJSpt9diaMdqnrnjLcy5PA'
        privateKey = '8swwLhnY6CUYS9v4L8yANcpftsG52xqrmygHJ4saTdSp'
        address = '3JrXMae8BFDUrVu6DxuQTvvEVf8NwxdnPct'
        expectedAccount = Account(address=address, publicKey=VerifyKey(base58.b58decode(publicKey)),
                                    privateKey=VerifyKey(base58.b58decode(privateKey)), seed=seed)
        account = self.factory.createFromSeed(seed, nonce=0)
        Tools().__eq__(expectedAccount, account)

    def testAssertAccountTrue(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        publicKey = VerifyKey(base58.b58decode('88Ny176gibcsKogkrkeR1MRJSpt9diaMdqnrnjLcy5PA'))
        privateKey = VerifyKey(base58.b58decode('8swwLhnY6CUYS9v4L8yANcpftsG52xqrmygHJ4saTdSp'))
        address = '3JrXMae8BFDUrVu6DxuQTvvEVf8NwxdnPct'
        account = Account(address=address, publicKey=publicKey, privateKey=privateKey, seed=seed)
        self.assertTrue(self.factory.assertAccount(account, address, publicKey, privateKey, seed))

    def testAssertAccountFalse(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        publicKey = VerifyKey(base58.b58decode('88Ny176gibcsKogkrkeR1MRJSpt9diaMdqnrnjLcy5PA'))
        privateKey = VerifyKey(base58.b58decode('8swwLhnY6CUYS9v4L8yANcpftsG52xqrmygHJ4saTdSp'))
        address = '3JrXMae8BFDUrVu6DxuQTvvEVf8NwxdnPct'
        account = Account(address='5JrXMae9BFDUrVu6DxuQTvvEVf8NwxdnPct', publicKey=publicKey, privateKey=privateKey, seed=seed)
        self.assertFalse(self.factory.assertAccount(account, address, publicKey, privateKey, seed))

    def testGenerateSeedPhrase(self):
        seedPhrase = self.factory.generateSeedPhrase()
        self.assertIs(15, len(seedPhrase.split()))

if __name__ == '__main__':
    unittest.main()
