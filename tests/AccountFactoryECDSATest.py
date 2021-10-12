from LTO.Accounts.AccountFactoryECDSA import AccountECDSA
import base58


class TestAccountECDSA():
    factory = AccountECDSA('L')
    seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
    account = factory.createFromSeed(seed)

    def testMakeKey(self):
        assert self.factory._MakeKey(self.seed).to_string() == (b'\xa7\x90:j\x80\xdb\x00}|~\x9e\x8cq]S\x97\x92\x97W\xfe\x17h>\xd5\xc1b\xa8\x1c|\x80\xc6%')

    def testCreateAddress(self):
        assert self.factory.createAddress(self.account.publicKey) == self.account.address

    def testCreateSignKeys(self):
        privateKey, publicKey = self.factory.createSignKeys(self.seed)
        assert self.account.publicKey == publicKey
        assert self.account.privateKey == privateKey

    def testCreateFromPublic(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        account = AccountECDSA('T').createFromSeed(seed)
        account2 = AccountECDSA('T').createFromPublicKey(account.publicKey)
        # object
        assert account.address == account2.address
        assert account.publicKey == account2.publicKey
        # bytes
        publicKey = b"5\xcf4\xeb\xe0\xd5,s\x00t\xc6to\x8b\xd0\x0e\xf8N\xe6\xa1\x1d\x13\x18s+\x11\x82\x7fR\x8d='\x03!a\x13H\xca=]\x8aV\xf71\x16C\x0c\x9ad{\x14z\x8e1\x9dg\x8b\xb2\xf2\x9e\x0fo\xa7\x9d"
        account3 = AccountECDSA('T').createFromPublicKey(publicKey)
        assert account.address == account3.address
        assert account.publicKey == account3.publicKey
        # b58 str
        account4 = AccountECDSA('T').createFromPublicKey(base58.b58encode(publicKey))
        assert account.address == account4.address
        assert account.publicKey == account4.publicKey


    def testCreateFromPrivateKey(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        account = AccountECDSA('T').createFromSeed(seed)
        account2 = AccountECDSA('T').createFromPrivateKey(account.privateKey)
        # object
        assert account.address == account2.address
        assert account.privateKey == account2.privateKey
        assert account.publicKey == account2.publicKey
        # bytes
        privateKey = b'\xa7\x90:j\x80\xdb\x00}|~\x9e\x8cq]S\x97\x92\x97W\xfe\x17h>\xd5\xc1b\xa8\x1c|\x80\xc6%'
        account3 = AccountECDSA('T').createFromPrivateKey(privateKey)
        assert account.address == account3.address
        assert account.privateKey == account3.privateKey
        assert account.publicKey == account3.publicKey
        # b58 str
        account4 = AccountECDSA('T').createFromPrivateKey(base58.b58encode(privateKey))
        assert account.address == account4.address
        assert account.privateKey == account4.privateKey
        assert account.publicKey == account4.publicKey

