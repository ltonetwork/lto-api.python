import base58
import unittest

from nacl.signing import VerifyKey
from lto.accounts.ed25519 import AccountFactory, Account
import pytest
from lto.accounts.brainwallet import random_seed as brainwallet_random_seed


class TestED25519(unittest.TestCase):
    factory = AccountFactory('T')
    seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
    account = AccountFactory('T').create_from_seed(seed)
    public_key_bytes = bytes(account.public_key)
    public_key_base58 = base58.b58encode(public_key_bytes)

    def test_create_address(self):
        expected = '3MyuPwbiobZFnZzrtyY8pkaHoQHYmyQxxY1'
        address = self.factory.create_address(
            public_key=VerifyKey(base58.b58decode("GjSacB6a5DFNEHjDSmn724QsrRStKYzkahPH67wyrhAY")))
        self.assertEqual(address, expected)

    def test_create_sign_keys(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        expected_public = '88Ny176gibcsKogkrkeR1MRJSpt9diaMdqnrnjLcy5PA'
        expected_private = '8swwLhnY6CUYS9v4L8yANcpftsG52xqrmygHJ4saTdSp'
        private_key, public_key, key_type = self.factory.create_sign_keys(seed)
        self.assertEqual(base58.b58encode(private_key.__bytes__()), expected_private)
        self.assertEqual(base58.b58encode(public_key.__bytes__()), expected_public)
        assert key_type == 'ed25519'

    def test_create_from_public(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        account = AccountFactory('T').create_from_seed(seed)
        account2 = AccountFactory('T').create_from_public_key(account.public_key)
        # object
        assert account.address == account2.address
        assert account.public_key == account2.public_key
        # bytes
        public_key = b'i\xe5\xb5\xee\xa8\x01OT\xc6\xb1\x15\xec_\x97\xcf\xe9b\xb7\xab&\xe3\x1bN\xc4\xb5\xe2\xd4\x9f\xab!\x98e'
        account3 = AccountFactory('T').create_from_public_key(base58.b58encode(public_key))
        assert account.address == account3.address
        assert account.public_key.__bytes__() == account3.public_key.__bytes__()
        # b58 str
        account4 = AccountFactory('T').create_from_public_key(base58.b58encode(public_key))
        assert account.address == account4.address
        assert account.public_key.__bytes__() == account4.public_key.__bytes__()

    def test_create_from_seed(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        address = '3N5EBTWWUvfBs3NCvAG51ovQnhASVfsVnv1'
        public_key = '88Ny176gibcsKogkrkeR1MRJSpt9diaMdqnrnjLcy5PA'
        private_key = '3Lk1yMwFTuujtqyy5HjaPqiBuyYcJaWgoupTpH1RxT8E4F619ThRoTnrZgBmhDyB44rKjnjExysRZHbXhKsQ5vr8'
        account = self.factory.create_from_seed(seed, nonce=0)
        assert account.address == address
        assert base58.b58encode(account.public_key.__bytes__()) == public_key
        assert base58.b58encode(account.private_key._signing_key) == private_key

    def testgenerate_seed(self):
        seedPhrase = brainwallet_random_seed()
        self.assertIs(15, len(seedPhrase.split()))

    def test_create_from_private_key(self):
        seed = 'fragile because fox snap picnic mean art observe vicious program chicken purse text hidden chest'
        account = self.factory.create_from_seed(seed)
        account2 = self.factory.create_from_private_key(account.private_key)
        assert account.address == account2.address
        assert account.public_key == account2.public_key
        assert account.private_key == account2.private_key

        private_key = '4sEbCdhpYrZuYGsGSNCR9mJrZgLY6kTdFMGDZnK3oQtSCjyvMz3K6ZMo1GfGmbqHK95Pwx6WTi7vMLpFGbsgbfqz'
        account3 = self.factory.create_from_private_key(private_key)
        assert account.address == account3.address
        assert account.public_key == account3.public_key
        assert account.private_key == account3.private_key
