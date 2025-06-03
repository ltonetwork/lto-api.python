from unittest import mock
from time import time
from lto.transactions.certificate import Certificate
from lto.accounts.ecdsa import AccountFactory
from freezegun import freeze_time
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509


class TestCertificate:
    account = AccountFactory('T', 'secp256r1').create_from_private_key(
        'AJQn2L4EhJhQh2NX5NvyDDB5BUPuiZBiNRmqRcSmj3g7'
    )
    cert_data = b"""-----BEGIN CERTIFICATE-----
MIIBmjCCAUGgAwIBAgIUBTg9WprxEdpxu8cLV2CKyGJ7bVQwCgYIKoZIzj0EAwIw
IzEhMB8GA1UEAwwYQWxpY2UsTz1FeGFtcGxlIEx0ZCxDPU5MMB4XDTI1MDYwMjEy
NTYzMloXDTI2MDYwMjEyNTYzMlowIzEhMB8GA1UEAwwYQWxpY2UsTz1FeGFtcGxl
IEx0ZCxDPU5MMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE2/WATtZvChbb3xrQ
EXzszXz3IgpUyA7jbLVQ9B2ibL/SZtvhjU84S8fI1HhzyE5eAqKvkh/pdArBjyXL
aqw0Q6NTMFEwHQYDVR0OBBYEFEb3OV2UesAgnXz8VOieyXgEilyHMB8GA1UdIwQY
MBaAFEb3OV2UesAgnXz8VOieyXgEilyHMA8GA1UdEwEB/wQFMAMBAf8wCgYIKoZI
zj0EAwIDRwAwRAIgVo0OBEFkXDgJGuIrOl15UKdkvrhe0THS8MO64Jw2F7cCIBpC
NLnbu23KWkzoIdACHRTGc3MqZrWh53lGq/+tK13P
-----END CERTIFICATE-----
"""

    def test_construct(self):
        tx = Certificate(self.cert_data)
        assert tx.tx_fee == 25000000
        assert tx.certificate.public_bytes(serialization.Encoding.PEM) == self.cert_data

    @freeze_time("2021-01-14")
    def test_sign_with(self):
        tx = Certificate(self.cert_data)
        assert not tx.is_signed()
        tx.sign_with(self.account)
        assert tx.is_signed()
        timestamp = int(time() * 1000)
        assert str(tx.timestamp)[:-3] == str(timestamp)[:-3]
        assert tx.sender == self.account.address
        assert self.account.verify(tx.to_binary(), tx.proofs[0])

    @freeze_time("2021-01-14")
    def test_to_json(self):
        tx = Certificate(self.cert_data)
        tx.timestamp = 1326499200000
        tx.sign_with(self.account)
        json = tx.to_json()
        assert json["type"] == 24
        assert json["version"] == 3
        assert json["sender"] == self.account.address
        assert json["certificate"] == self.cert_data.decode()

    @mock.patch('src.lto.PublicNode')
    def test_broadcast(self, mock_PublicNode):
        tx = Certificate(self.cert_data)
        broadcasted_tx = Certificate(self.cert_data)
        broadcasted_tx.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_PublicNode.return_value
        mc.broadcast.return_value = broadcasted_tx
        assert mc.broadcast(tx) == broadcasted_tx

    @freeze_time("2021-01-14")
    def test_from_data(self):
        data = {
            "type": 24,
            "version": 3,
            "id": "2GqzNqFvxRQh7DQENecUj6kQMsA6JPXjvS7p1yx7PePx",
            "sender": self.account.address,
            "senderKeyType": self.account.key_type,
            "senderPublicKey": self.account.get_public_key(),
            "fee": 25000000,
            "timestamp": 1326499200000,
            "certificate": self.cert_data.decode(),
            "proofs": ["2omugkAQdrm9P7YPx6WZbXMBTifRS6ptaTT8rPRRvKFr1EPFafHSosq6HzkuuLv78gR6vaXLA9WtMsTSBgi3H1qe"],
            "height": 1070000
        }

        tx = Certificate.from_data(data)

        assert isinstance(tx, Certificate)
        assert tx.version == 3
        assert tx.id == data["id"]
        assert tx.sender == data["sender"]
        assert tx.sender_key_type == data["senderKeyType"]
        assert tx.sender_public_key == data["senderPublicKey"]
        assert tx.tx_fee == data["fee"]
        assert tx.timestamp == data["timestamp"]
        assert tx.proofs == data["proofs"]
        assert tx.height == data["height"]

        expected_cert = x509.load_pem_x509_certificate(self.cert_data)
        assert tx.certificate.fingerprint(hashes.SHA256()) == expected_cert.fingerprint(hashes.SHA256())
