import math
import base58
import struct
from lto import crypto
from lto.binary import Binary
from lto.transaction import Transaction
from lto.transactions.data_entry import DataEntry, dict_to_data


class Association(Transaction):
    BASE_FEE = 50000000
    VAR_FEE = 10000000
    VAR_BYTES = 256
    TYPE = 16
    DEFAULT_VERSION = 3

    def __init__(self,
                 association_type: int,
                 recipient: str,
                 subject: bytes = None,
                 expires: int = None,
                 data=None):
        super().__init__()

        self.version = self.DEFAULT_VERSION
        self.recipient = recipient
        self.association_type = association_type
        self.subject = Binary(subject or b'')
        self.expires = expires
        self.data = dict_to_data(data) if type(data) == dict else (data or [])
        self.tx_fee = self.BASE_FEE + math.ceil((len(self.__data_to_binary()) / self.VAR_BYTES)) * self.VAR_FEE

    def __data_to_binary(self):
        binary = b''
        for entry in self.data:
            binary += entry.to_binary()
        return binary

    def __to_binary_v1(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\1' +
                crypto.str2bytes(self.chain_id) +
                base58.b58decode(self.sender_public_key) +
                base58.b58decode(self.recipient) +
                struct.pack(">i", self.association_type) +
                (b'\1' + struct.pack(">H", len(self.subject)) + self.subject if self.subject else b'\0') +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.tx_fee))

    def __to_binary_v3(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                base58.b58decode(self.recipient) +
                struct.pack(">i", self.association_type) +
                struct.pack(">Q", self.expires or 0) +
                struct.pack(">H", len(self.subject)) +
                self.subject)

    def __to_binary_v4(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\4' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">Q", self.association_type) +
                base58.b58decode(self.recipient) +
                struct.pack(">Q", self.expires or 0) +
                struct.pack(">H", len(self.subject)) +
                self.subject +
                struct.pack(">H", len(self.data)) +
                self.__data_to_binary())

    def to_binary(self):
        if self.version == 1:
            return self.__to_binary_v1()
        elif self.version == 3:
            return self.__to_binary_v3()
        elif self.version == 4:
            return self.__to_binary_v4()
        else:
            raise Exception('Incorrect Version')

    def data_as_dict(self):
        dictionary = {}
        for entry in self.data:
            dictionary[entry.key] = entry.value
        return dictionary

    def to_json(self):
        return crypto.clean_dict({
            "id": self.id,
            "type": self.TYPE,
            "version": self.version,
            "sender": self.sender,
            "senderKeyType": self.sender_key_type,
            "senderPublicKey": self.sender_public_key,
            "associationType": self.association_type,
            "recipient": self.recipient,
            "subject": self.subject.base58() if self.subject else None,
            "timestamp": self.timestamp,
            "expires": self.expires,
            "data": [entry.to_json() for entry in self.data] if self.data else None,
            "fee": self.tx_fee,
            "sponsor": self.sponsor,
            "sponsorKeyType": self.sponsor_key_type,
            "sponsorPublicKey": self.sponsor_public_key,
            "proofs": self.proofs or None,
            "height": self.height
        })

    @staticmethod
    def from_data(data):
        tx = Association(
            data['associationType'],
            data['recipient'],
            Binary.frombase58(data.get('subject', '')),
            data.get('expires'),
            [DataEntry.from_data(entry) for entry in data.get('data', [])]
        )
        tx._init_from_data(data)

        return tx
