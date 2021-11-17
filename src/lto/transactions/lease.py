import base58
from lto import crypto
import struct
from lto.transaction import Transaction

class Lease(Transaction):
    DEFAULT_LEASE_FEE = 100000000
    TYPE = 8
    DEFAULT_VERSION = 3

    def __init__(self, recipient, amount):
        super().__init__()
        self.amount = amount
        self.recipient = recipient
        self.tx_fee = self.DEFAULT_LEASE_FEE
        self.version = self.DEFAULT_VERSION
        if self.amount <= 0:
            raise Exception ('Amount must be > 0')


    def __to_binary_V2(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\2' +
                b'\0' +
                base58.b58decode(self.sender_public_key) +
                base58.b58decode(self.recipient) +
                struct.pack(">Q", self.amount) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">Q", self.timestamp))

    def __to_binary_V3(self):
        return (
                self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                base58.b58decode(self.recipient) +
                struct.pack(">Q", self.amount)
        )

    def to_binary(self):
        if self.version == 2:
            return self.__to_binary_V2()
        elif self.version == 3:
            return self.__to_binary_V3()
        else:
            raise Exception('Incorrect Version')

    def to_json(self):
        return ({
            "type": self.TYPE,
            "version": self.version,
            "sender": self.sender,
            "senderKeyType": self.sender_key_type,
            "senderPublicKey": self.sender_public_key,
            "recipient": self.recipient,
            "amount": self.amount,
            "fee": self.tx_fee,
            "timestamp": self.timestamp,
            "proofs": self.proofs
        } | self._sponsor_json())

    @staticmethod
    def from_data(data):
        tx = Lease('',1)
        tx.id = data['id'] if 'id' in data else ''
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.sender_key_type = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.sender_public_key = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.recipient = data['recipient']
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.height = data['height'] if 'height' in data else ''
        return tx



