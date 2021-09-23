from unittest import mock
from LTO.Transactions.Transfer import Transfer
from LTO.AccountFactory import AccountFactory
from time import time
import pytest

class TestTransaction:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    ACCOUNT2_SEED = "cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy"

    account = AccountFactory('T').createFromSeed(ACCOUNT_SEED)
    account2 = AccountFactory('T').createFromSeed(ACCOUNT2_SEED)


    def testSponsorWith(self):
        transaction = Transfer('3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb', 10000)
        with pytest.raises(Exception):
            transaction.sponsorWith(self.account2)
        transaction.signWith(self.account)

        transaction.sponsorWith(self.account2)
        assert transaction.sponsor == self.account2.address
        assert transaction.sponsorPublicKey == self.account2.publicKey
        assert transaction.sponsorKeyType == 'ed25519'

        assert self.account2.verifySignature(transaction.toBinary(), transaction.proofs[1])

        json = transaction.toJson()
        assert json['sponsor'] == self.account2.address
        assert json['sponsorPublicKey'] == self.account2.publicKey
        assert json['sponsorKeyType'] == 'ed25519'

