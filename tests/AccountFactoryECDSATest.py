from LTO.Accounts.AccountFactoryECDSA import AccountECDSA as AccountFactory
from LTO.tools import Tools


class TestAccountECDSA():
    factory = AccountFactory('L')
    seed = 'curtain want coffee other panel satoshi tissue chief floor lumber size dinner upper verb wall'
    account = factory.createFromSeed(seed)

    def testMakeKey(self):
        assert self.factory._MakeKey(self.seed).to_string() == b"\xa4\xd12%\xff\xb9\x89\xfc7 \t^\x97\xdd\x9a(r\x10'\x0f\x85\xca\x11Jb=Pn\xfd\xab\xb1\x1d"

    def testCreateAddress(self):
        assert self.factory.createAddress(self.account.publicKey) == self.account.address

    def testCreateSignKeys(self):
        privateKey, publicKey = self.factory.createSignKeys(self.seed)
        assert self.account.publicKey == publicKey
        assert self.account.privateKey == privateKey

    def testCreateFromPublic(self):
        account = self.factory.createFromPublicKey(self.account.publicKey)
        Tools().__eq__(account, self.account)

        account = self.factory.createFromPublicKey(self.account.publicKey.to_string())
        Tools().__eq__(account, self.account)

    def testCreateFromPrivateKey(self):
        account = self.factory.createFromPrivateKey(self.account.privateKey)
        Tools().__eq__(account, self.account)

        account = self.factory.createFromPrivateKey(self.account.privateKey.to_string())
        Tools().__eq__(account, self.account)
