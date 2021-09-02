import base58
from PyCLTO import crypto
import struct
from time import time
from PyCLTO.Transaction import Transaction
from PyCLTO.Account import Account


class Anchor(Transaction):
    TYPE = 15
    DEFAULT_ANCHOR_FEE = 35000000

    def __init__(self, anchor):
        super().__init__()

        self.anchor = anchor
        self.txFee = self.DEFAULT_ANCHOR_FEE

    def toBinary(self):
        return(b'\x0f' +
                    b'\1' +
                    base58.b58decode(self.senderPublicKey) +
                    struct.pack(">H", 1) +
                    struct.pack(">H", len(crypto.str2bytes(self.anchor))) +
                    crypto.str2bytes(self.anchor) +
                    struct.pack(">Q", self.timestamp) +
                    struct.pack(">Q", self.txFee))

    def toJson(self):
        return({
                "type": self.TYPE,
                "version": 1,
                "senderPublicKey": self.senderPublicKey,
                "anchors": base58.b58encode(crypto.str2bytes(self.anchor)),
                "fee": self.txFee,
                "timestamp": self.timestamp,
                "proofs":
                    self.proofs

            })

    @staticmethod
    def fromData(data):
        tx = Anchor(anchor='')
        tx.id = data['id']
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender']
        tx.senderPublicKey = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.anchors = data['anchors']
        tx.proofs = data['proofs']
        if 'height' in data:
            tx.height = data['height']
        return tx
