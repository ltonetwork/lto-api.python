import base58
import struct
from lto import crypto
from lto.transaction import Transaction
from lto.transactions.data_entry import DataEntry, dict_to_data


class Association(Transaction):
    DEFAULT_FEE = 100000000
    TYPE = 16
    DEFAULT_VERSION = 3

    def __init__(self, recipient, association_type, subject=None, expires=None, data=None):
        super().__init__()
        self.recipient = recipient
        self.association_type = association_type
        self.subject = subject
        self.tx_fee = self.DEFAULT_FEE
        self.version = self.DEFAULT_VERSION
        self.expires = expires
        self.data = dict_to_data(data) if type(data) == dict else (data or [])

    def __data_to_binary(self):
        binary = b''
        for entry in self.data:
            binary += entry.to_binary()
        return binary

    def __to_binary_v1(self):
        subject_bytes = crypto.str2bytes(self.subject or '')
        return (self.TYPE.to_bytes(1, 'big') +
                b'\1' +
                crypto.str2bytes(self.chain_id) +
                base58.b58decode(self.sender_public_key) +
                base58.b58decode(self.recipient) +
                struct.pack(">i", self.association_type) +
                (b'\1' + struct.pack(">H", len(subject_bytes)) + subject_bytes if self.subject else b'\0') +
                subject_bytes +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.tx_fee))

    def __to_binary_v3(self):
        subject_bytes = crypto.str2bytes(self.subject or '')
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
                struct.pack(">H", len(subject_bytes)) +
                subject_bytes)

    def __to_binary_v4(self):
        return (self.__to_binary_v3() +
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
            "recipient": self.recipient,
            "associationType": self.association_type,
            "subject": base58.b58encode(crypto.str2bytes(self.subject)),
            "timestamp": self.timestamp,
            "expires": self.expires,
            "data": self.data,
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
            data['recipient'],
            data['associationType'],
            data.get('subject'),
            list(map(DataEntry.from_data, data['data'])) if 'data' in data else []
        )
        tx._init_from_data(data)

        return tx
