from lto.accounts import AccountFactoryECDSA
import base58
import pytest


class TestAccountECDSA():
    factory = AccountFactoryECDSA('L')
    seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
    account = factory.create()

    def test_make_key(self):
        assert self.factory._MakeKey(self.seed).to_string() == (b'\xa7\x90:j\x80\xdb\x00}|~\x9e\x8cq]S\x97\x92\x97W\xfe\x17h>\xd5\xc1b\xa8\x1c|\x80\xc6%')

    @pytest.mark.skip(reason="Secp256k1 under construction")
    def test_create_address(self):
        assert self.factory.create_address(self.account.public_key) == self.account.address

    @pytest.mark.skip(reason="Secp256k1 under construction")
    def test_create_sign_keys(self):
        private_key, public_key, key_type = self.factory.create_sign_keys(self.seed)
        assert self.account.public_key == public_key
        assert self.account.private_key == private_key
        assert key_type == 'secp256k1'

    @pytest.mark.skip(reason="Secp256k1 under construction")
    def test_create_from_public(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        account = AccountFactoryECDSA('T').create_from_seed(seed)
        account2 = AccountFactoryECDSA('T').create_from_public_key(account.public_key)
        # object
        assert account.address == account2.address
        assert account.public_key == account2.public_key
        # bytes
        public_key = b"5\xcf4\xeb\xe0\xd5,s\x00t\xc6to\x8b\xd0\x0e\xf8N\xe6\xa1\x1d\x13\x18s+\x11\x82\x7fR\x8d='\x03!a\x13H\xca=]\x8aV\xf71\x16C\x0c\x9ad{\x14z\x8e1\x9dg\x8b\xb2\xf2\x9e\x0fo\xa7\x9d"
        account3 = AccountFactoryECDSA('T').create_from_public_key(public_key)
        assert account.address == account3.address
        assert account.public_key == account3.public_key
        # b58 str
        account4 = AccountFactoryECDSA('T').create_from_public_key(base58.b58encode(public_key))
        assert account.address == account4.address
        assert account.public_key == account4.public_key

    @pytest.mark.skip(reason="Secp256k1 under construction")
    def test_create_from_private_key(self):
        seed = 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep'
        account = AccountFactoryECDSA('T').create_from_seed(seed)
        account2 = AccountFactoryECDSA('T').create_from_private_key(account.private_key)
        # object
        assert account.address == account2.address
        assert account.private_key == account2.private_key
        assert account.public_key == account2.public_key
        # bytes
        private_key = b'\xa7\x90:j\x80\xdb\x00}|~\x9e\x8cq]S\x97\x92\x97W\xfe\x17h>\xd5\xc1b\xa8\x1c|\x80\xc6%'
        account3 = AccountFactoryECDSA('T').create_from_private_key(private_key)
        assert account.address == account3.address
        assert account.private_key == account3.private_key
        assert account.public_key == account3.public_key
        # b58 str
        account4 = AccountFactoryECDSA('T').create_from_private_key(base58.b58encode(private_key))
        assert account.address == account4.address
        assert account.private_key == account4.private_key
        assert account.public_key == account4.public_key

