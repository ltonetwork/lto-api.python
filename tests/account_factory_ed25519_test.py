import base58
import unittest

from nacl.signing import VerifyKey

from lto.accounts.account_factory_ed25519 import AccountFactoryED25519
from lto.account import Account
from lto.tools import Tools


class AccountTest(unittest.TestCase):
    factory = AccountFactoryED25519('L')

    def testcreate_address(self):
        expected = '3JmCa4jLVv7Yn2XkCnBUGsa7WNFVEMxAfWe'
        address = self.factory.create_address(
            public_key=VerifyKey(base58.b58decode("GjSacB6a5DFNEHjDSmn724QsrRStKYzkahPH67wyrhAY")))
        self.assertEqual(address, expected)

    def testcreate_sign_keys(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        expectedPublic = '88Ny176gibcsKogkrkeR1MRJSpt9diaMdqnrnjLcy5PA'
        expectedPrivate = '8swwLhnY6CUYS9v4L8yANcpftsG52xqrmygHJ4saTdSp'
        private_key, public_key = self.factory.create_sign_keys(seed)
        self.assertEqual(base58.b58encode(private_key.__bytes__()), expectedPrivate)
        self.assertEqual(base58.b58encode(public_key.__bytes__()), expectedPublic)

    def testCreateFromPublic(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        account = AccountFactoryED25519('T').create_from_seed(seed)
        account2 = AccountFactoryED25519('T').create_from_public_key(account.public_key)
        # object
        assert account.address == account2.address
        assert account.public_key == account2.public_key
        # bytes
        public_key = b'i\xe5\xb5\xee\xa8\x01OT\xc6\xb1\x15\xec_\x97\xcf\xe9b\xb7\xab&\xe3\x1bN\xc4\xb5\xe2\xd4\x9f\xab!\x98e'
        account3 = AccountFactoryED25519('T').create_from_public_key(base58.b58encode(public_key))
        assert account.address == account3.address
        assert account.public_key.__bytes__() == base58.b58decode(account3.public_key)
        # b58 str
        account4 = AccountFactoryED25519('T').create_from_public_key(base58.b58encode(public_key))
        assert account.address == account4.address
        assert account.public_key.__bytes__() == base58.b58decode(account4.public_key)

    def testcreate_from_seed(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        public_key = '88Ny176gibcsKogkrkeR1MRJSpt9diaMdqnrnjLcy5PA'
        private_key = '8swwLhnY6CUYS9v4L8yANcpftsG52xqrmygHJ4saTdSp'
        address = '3JrXMae8BFDUrVu6DxuQTvvEVf8NwxdnPct'
        expectedAccount = Account(address=address, public_key=VerifyKey(base58.b58decode(public_key)),
                                    private_key=VerifyKey(base58.b58decode(private_key)), seed=seed)
        account = self.factory.create_from_seed(seed, nonce=0)
        assert account.address == address
        assert base58.b58encode(account.public_key.__bytes__()) == public_key
        assert base58.b58encode(account.private_key.__bytes__()) == private_key
        assert account.seed == account.seed

    def testAssertAccountTrue(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        public_key = VerifyKey(base58.b58decode('88Ny176gibcsKogkrkeR1MRJSpt9diaMdqnrnjLcy5PA'))
        private_key = VerifyKey(base58.b58decode('8swwLhnY6CUYS9v4L8yANcpftsG52xqrmygHJ4saTdSp'))
        address = '3JrXMae8BFDUrVu6DxuQTvvEVf8NwxdnPct'
        account = Account(address=address, public_key=public_key, private_key=private_key, seed=seed)

    def testAssertAccountFalse(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        public_key = VerifyKey(base58.b58decode('88Ny176gibcsKogkrkeR1MRJSpt9diaMdqnrnjLcy5PA'))
        private_key = VerifyKey(base58.b58decode('8swwLhnY6CUYS9v4L8yANcpftsG52xqrmygHJ4saTdSp'))
        address = '3JrXMae8BFDUrVu6DxuQTvvEVf8NwxdnPct'
        account = Account(address='5JrXMae9BFDUrVu6DxuQTvvEVf8NwxdnPct', public_key=public_key, private_key=private_key, seed=seed)

    def testgenerate_seed(self):
        seedPhrase = self.factory.generate_seed()
        self.assertIs(15, len(seedPhrase.split()))

    def testcreate_from_private_key(self):
        seed = 'fragile because fox snap picnic mean art observe vicious program chicken purse text hidden chest'
        account = AccountFactoryED25519('T').create_from_seed(seed)
        account2 = AccountFactoryED25519('T').create_from_private_key(account.private_key)
        assert account.address == account2.address
        assert account.public_key == account2.public_key
        assert account.private_key == account2.private_key

        private_key = '4sEbCdhpYrZuYGsGSNCR9mJrZgLY6kTdFMGDZnK3oQtSCjyvMz3K6ZMo1GfGmbqHK95Pwx6WTi7vMLpFGbsgbfqz'
        account3 = AccountFactoryED25519('T').create_from_private_key(private_key)
        assert account.address == account3.address
        assert account.public_key == account3.public_key
        assert account.private_key.__bytes__() == account3.private_key

