import base58
import struct
from lto import crypto
from lto.transaction import Transaction
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from typing import Union, Optional

class Certificate(Transaction):
    TYPE = 24
    BASE_FEE = 500000000
    DEFAULT_VERSION = 3

    def __init__(self, cert: Optional[Union[bytes, str]]):
        super().__init__()

        if cert is None:
            self.certificate = None
        elif self._is_pem(cert):
            if isinstance(cert, str):
                cert = cert.encode()
            self.certificate = x509.load_pem_x509_certificate(cert)
        else:
            self.certificate = x509.load_der_x509_certificate(cert)

        self.tx_fee = self.BASE_FEE
        self.version = self.DEFAULT_VERSION

    def __to_binary_v3(self):
        der_bytes = b"" if self.certificate is None else self.certificate.public_bytes(encoding=serialization.Encoding.DER)

        return (
            self.TYPE.to_bytes(1, 'big') +
            b'\3' +
            crypto.str2bytes(self.chain_id) +
            struct.pack(">Q", self.timestamp) +
            crypto.key_type_id(self.sender_key_type) +
            base58.b58decode(self.sender_public_key) +
            struct.pack(">Q", self.tx_fee) +
            struct.pack(">H", len(der_bytes)) +
            der_bytes
        )

    def to_binary(self):
        if self.version == 3:
            return self.__to_binary_v3()
        raise Exception(f'Unsupported version: {self.version}')

    def to_json(self):
        return crypto.clean_dict({
            "id": self.id,
            "type": self.TYPE,
            "version": self.version,
            "sender": self.sender,
            "senderKeyType": self.sender_key_type,
            "senderPublicKey": self.sender_public_key,
            "fee": self.tx_fee,
            "timestamp": self.timestamp,
            "certificate": None if self.certificate is None else self.certificate.public_bytes(serialization.Encoding.PEM).decode(),
            "sponsor": self.sponsor,
            "sponsorKeyType": self.sponsor_key_type,
            "sponsorPublicKey": self.sponsor_public_key,
            "proofs": self.proofs or None,
            "height": self.height
        })

    @staticmethod
    def from_data(data):
        tx = Certificate(data["certificate"])
        tx._init_from_data(data)
        return tx

    @staticmethod
    def _is_pem(cert):
        return isinstance(cert, (bytes, str)) and b"-----BEGIN CERTIFICATE-----" in cert \
            if isinstance(cert, bytes) else "-----BEGIN CERTIFICATE-----" in cert
