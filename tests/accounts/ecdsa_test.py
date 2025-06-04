import pytest
from lto.accounts.ecdsa.account_factory_ecdsa import AccountFactoryECDSA

class TestECDSA:
    factory = AccountFactoryECDSA('L', 'secp256k1')
    factoryP256 = AccountFactoryECDSA('P', 'secp256r1')
    seed = 'satisfy sustain shiver skill betray mother appear pupil coconut weasel firm top puzzle monkey seek'
    priv_key_b58 = 'DRpStYEzVkHs8WRGz9zcxRoudhnYzeGzJ6JVVWFcrbsA'
    pub_key_b58 = 'yBUTnq2bLomxJSrQTMgD9CLKLLzKxZCMTH2naizoBpcZ'
    message = b'hello'

    def test_from_seed(self):
        account = self.factory.create_from_seed(self.seed)
        assert account.key_type == 'secp256k1'
        assert account.seed == self.seed
        assert account.nonce == 0
        assert account.get_private_key() == self.priv_key_b58
        assert account.get_public_key() == self.pub_key_b58

    def test_sign_and_verify(self):
        account = self.factory.create_from_seed(self.seed)
        sig = account.sign(self.message)
        assert account.verify(self.message, sig)

    def test_from_private_key(self):
        account = self.factory.create_from_private_key(self.priv_key_b58)
        assert account.key_type == 'secp256k1'
        assert account.get_private_key() == self.priv_key_b58
        assert account.get_public_key() == self.pub_key_b58

    def test_from_public_key(self):
        account = self.factory.create_from_public_key(self.pub_key_b58)
        assert account.key_type == 'secp256k1'
        assert account.get_public_key() == self.pub_key_b58

    def test_from_private_key_pem(self):
        pem = b"""-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIIou8KM/HGKYJclB1jfLOb6bmL/5ARlYDStwnslUk3/UoAoGCCqGSM49
AwEHoUQDQgAE2/WATtZvChbb3xrQEXzszXz3IgpUyA7jbLVQ9B2ibL/SZtvhjU84
S8fI1HhzyE5eAqKvkh/pdArBjyXLaqw0Qw==
-----END EC PRIVATE KEY-----"""
        account = self.factoryP256.create_from_private_key(pem)
        assert account.key_type == 'secp256r1'
        assert account.get_private_key() == 'AJQn2L4EhJhQh2NX5NvyDDB5BUPuiZBiNRmqRcSmj3g7'
        assert account.get_public_key() == '29VaXAx2ac63f5sjHHXyB4FJMLi3QrLj3r5mmLFaNy85k'

    def test_from_public_key_pem(self):
        pem = b"""-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE2/WATtZvChbb3xrQEXzszXz3IgpU
yA7jbLVQ9B2ibL/SZtvhjU84S8fI1HhzyE5eAqKvkh/pdArBjyXLaqw0Qw==
-----END PUBLIC KEY-----"""
        account = self.factoryP256.create_from_public_key(pem)
        assert account.key_type == 'secp256r1'
        assert account.get_public_key() == '29VaXAx2ac63f5sjHHXyB4FJMLi3QrLj3r5mmLFaNy85k'
