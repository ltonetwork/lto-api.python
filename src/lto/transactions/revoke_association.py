import base58
from lto import crypto
from lto.transaction import Transaction
import struct

class RevokeAssociation(Transaction):
    TYPE = 17
    DEFAULT_LEASE_FEE = 100000000
    DEFAULT_VERSION = 3

    def __init__(self, recipient, association_type, anchor = ''):
        super().__init__()
        self.recipient = recipient
        self.anchor = anchor
        self.association_type = association_type

        self.tx_fee = self.DEFAULT_LEASE_FEE
        self.version = self.DEFAULT_VERSION

    def __to_binary_V1(self):
        if self.anchor:
            return (self.TYPE.to_bytes(1, 'big') +
                    b'\1' +
                    crypto.str2bytes(crypto.get_network(self.sender)) +
                    base58.b58decode(self.sender_public_key) +
                    base58.b58decode(self.recipient) +
                    struct.pack(">i", self.association_type) +
                    b'\1' +
                    struct.pack(">H", len(crypto.str2bytes(self.anchor))) +
                    crypto.str2bytes(self.anchor) +
                    struct.pack(">Q", self.timestamp) +
                    struct.pack(">Q", self.tx_fee))
        else:
            return (self.TYPE.to_bytes(1, 'big') +
                    b'\1' +
                    crypto.str2bytes(crypto.get_network(self.sender)) +
                    base58.b58decode(self.sender_public_key) +
                    base58.b58decode(self.recipient) +
                    struct.pack(">i", self.association_type) +
                    b'\0' +
                    struct.pack(">Q", self.timestamp) +
                    struct.pack(">Q", self.tx_fee))


    def __to_binary_V3(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                base58.b58decode(self.recipient) +
                struct.pack(">i", self.association_type) +
                struct.pack(">H", len(crypto.str2bytes(self.anchor))) +
                crypto.str2bytes(self.anchor)
                )

    def to_binary(self):
        if self.version == 1:
            return self.__to_binary_V1()
        elif self.version == 3:
            return self.__to_binary_V3()
        else:
            raise Exception('Incorrect Version')

    def to_json(self):
        return ({
            "type": self.TYPE,
            "version": self.version,
            "sender": self.sender_public_key,
            "senderKeyType": self.sender_key_type,
            "senderPublicKey": self.sender_public_key,
            "recipient": self.recipient,
            "associationType": self.association_type,
            "hash": base58.b58encode(crypto.str2bytes(self.anchor)),
            "timestamp": self.timestamp,
            "fee": self.tx_fee,
            "proofs": self.proofs
        } | self._sponsor_json())

    @staticmethod
    def from_data(data):
        tx = RevokeAssociation(recipient='', association_type='')
        tx.type = data['type']
        tx.version = data['version']
        tx.id = data['id'] if 'id' in data else ''
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.sender_key_type = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.sender_public_key = data['senderPublicKey']
        tx.recipient = data['party'] if 'party' in data else data['recipient']
        tx.association_type = data['associationType']
        tx.hash = data['hash'] if 'hash' in data else ''
        tx.timestamp = data['timestamp']
        tx.fee = data['fee']
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.height = data['height'] if 'height' in data else ''
        return tx