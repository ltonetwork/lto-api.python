import base58
import struct
from lto import crypto
from lto.transaction import Transaction
from lto.transactions.data import DataEntry


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
        self.data = self.__dict_to_data(data) if type(data) == dict else (data or [])

    @staticmethod
    def __dict_to_data(dictionary):
        data = []
        for key in dictionary:
            data.append(DataEntry.guess(key, dictionary[key]))
        return data

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
                (b'\1' + struct.pack(">H", len(subject_bytes)) if self.subject else b'\0') +
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
        tx = Association(None, None)
        tx.type = data['type']
        tx.version = data['version']
        tx.id = data.get('id', None)
        tx.sender = data.get('sender', None)
        tx.sender_key_type = data.get('senderKeyType', None)
        tx.sender_public_key = data.get('senderPublicKey', None)
        tx.recipient = data['recipient']
        tx.association_type = data['associationType']
        tx.subject = data.get('subject', None)
        tx.data = list(map(DataEntry.from_data, data['data'])) if 'data' in data else []
        tx.timestamp = data['timestamp']
        tx.expires = data.get('expires', None)
        tx.fee = data['fee']
        tx.proofs = data.get('proofs', [])
        tx.height = data.get('height', None)
        tx.sponsor = data.get('sponsor', None)
        tx.sponsor_public_key = data.get('sponsorPublicKey', None)
        tx.sponsor_key_type = data.get('sponsorKeyType', None)

        return tx
