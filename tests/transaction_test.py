from lto.transactions.transfer import Transfer
from lto.accounts.ed25519.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
import pytest
import base58


class TestTransaction:
    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    ACCOUNT2_SEED = "cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy"

    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)
    account2 = AccountFactory('T').create_from_seed(ACCOUNT2_SEED)

    def test_sponsor_with(self):
        transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 10000)
        with pytest.raises(Exception):
            transaction.sponsor_with(self.account2)
        transaction.sign_with(self.account)

        transaction.sponsor_with(self.account2)
        assert transaction.sponsor == self.account2.address
        assert transaction.sponsor_public_key == base58.b58encode(self.account2.public_key.__bytes__())
        assert transaction.sponsor_key_type == 'ed25519'

        assert self.account2.verify_signature(transaction.to_binary(), transaction.proofs[1])

        json = transaction.to_json()
        assert json['sponsor'] == self.account2.address
        assert json['sponsorPublicKey'] == base58.b58encode(self.account2.public_key.__bytes__())
        assert json['sponsorKeyType'] == self.account2.key_type
