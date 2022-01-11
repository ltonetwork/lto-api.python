from lto import LTO
from lto.public_node import PublicNode
from lto.accounts.ed25519 import Account, VerifyKey, SigningKey
import base58

class TestInit:
    expected_account = Account(
        seed='fragile because fox snap picnic mean art observe vicious program chicken purse text hidden chest',
        address='3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj',
        public_key=VerifyKey(base58.b58decode('G3PaJt9cUvM5dVW8XAZnKrqmQj1xbSQ4yM7gWuknEKjn')),
        private_key=SigningKey(base58.b58decode('4sEbCdhpYrZuYGsGSNCR9mJrZgLY6kTdFMGDZnK3oQtSCjyvMz3K6ZMo1GfGmbqHK95Pwx6WTi7vMLpFGbsgbfqz')[:-32])
    )

    def test_construct_testnet(self):
        lto = LTO()
        assert lto.NODE.url == PublicNode('https://testnet.lto.network').url
        assert lto.chain_id == 'T'

    def test_construct_mainnet(self):
        lto = LTO('L')
        assert lto.NODE.url == PublicNode('https://nodes.lto.network').url
        assert lto.chain_id == 'L'

    def test_construct_custom(self):
        lto = LTO('Z')
        assert lto.NODE == ''
        assert lto.chain_id == 'Z'

    def test_account_from_seed(self):
        lto = LTO()
        account = lto.Account(seed=self.expected_account.seed)
        assert self.expected_account.address == account.address
        assert self.expected_account.seed == account.seed
        assert self.expected_account.get_public_key() == account.get_public_key()
        assert self.expected_account.get_private_key() == account.get_private_key()

    def test_account_from_public_key(self):
        lto = LTO()
        account = lto.Account(public_key=self.expected_account.public_key)
        assert self.expected_account.address == account.address
        assert self.expected_account.get_public_key() == account.get_public_key()

    def test_account_random(self):
        lto = LTO()
        assert lto.Account()
