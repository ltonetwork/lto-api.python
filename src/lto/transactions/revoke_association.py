import base58
from lto import crypto
from lto.transaction import Transaction
import struct

class RevokeAssociation(Transaction):
    TYPE = 17
    DEFAULT_FEE = 100000000
    DEFAULT_VERSION = 3

    def __init__(self, recipient, association_type, subject = None):
        super().__init__()
        self.recipient = recipient
        self.subject = subject
        self.association_type = association_type

        self.tx_fee = self.DEFAULT_FEE
        self.version = self.DEFAULT_VERSION

    def __to_binary_v1(self):
        subject_bytes = crypto.str2bytes(self.subject or '')
        return (self.TYPE.to_bytes(1, 'big') +
                b'\1' +
                crypto.str2bytes(crypto.get_network(self.sender)) +
                base58.b58decode(self.sender_public_key) +
                base58.b58decode(self.recipient) +
                struct.pack(">i", self.association_type) +
                (b'\1' + struct.pack(">H", len(subject_bytes)) + subject_bytes if self.subject else b'\0') +
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
                struct.pack(">H", len(crypto.str2bytes(self.subject))) +
                crypto.str2bytes(self.subject))

    def to_binary(self):
        if self.version == 1:
            return self.__to_binary_v1()
        elif self.version == 3:
            return self.__to_binary_v3()
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
            "fee": self.tx_fee,
            "sponsor": self.sponsor,
            "sponsorKeyType": self.sponsor_key_type,
            "sponsorPublicKey": self.sponsor_public_key,
            "proofs": self.proofs or None,
            "height": self.height
        })

    @staticmethod
    def from_data(data):
        tx = RevokeAssociation(data['recipient'], data['association_type'], data.get('subject'))
        tx._init_from_data(data)

        return tx
