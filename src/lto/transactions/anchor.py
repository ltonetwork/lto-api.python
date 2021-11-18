import base58
from lto import crypto
from lto.transaction import Transaction
import struct

class Anchor(Transaction):
    TYPE = 15
    DEFAULT_ANCHOR_FEE = 35000000
    DEFAULT_VERSION = 3

    def __init__(self, anchor):
        super().__init__()

        self.anchor = anchor
        self.tx_fee = self.DEFAULT_ANCHOR_FEE
        self.version = self.DEFAULT_VERSION


    def __to_binary_V1(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\1' +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">H", 1) +
                struct.pack(">H", len(crypto.str2bytes(self.anchor))) +
                crypto.str2bytes(self.anchor) +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.tx_fee))

    def __to_binary_V3(self):
        return (
                self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">H", 1) +
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
        return({
            "type": self.TYPE,
            "version": self.version,
            "sender": self.sender,
            "senderKeyType": self.sender_key_type,
            "senderPublicKey": self.sender_public_key,
            "fee": self.tx_fee,
            "timestamp": self.timestamp,
            "anchors": [base58.b58encode(crypto.str2bytes(self.anchor))],
            "proofs": self.proofs
            } | self._sponsor_json())

    @staticmethod
    def from_data(data):
        tx = Anchor(anchor='')
        tx.id = data['id'] if 'id' in data else ''
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.sender_key_type = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.sender_public_key = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.anchors = data['anchors']
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.height = data['height'] if 'height' in data else ''
        return tx
