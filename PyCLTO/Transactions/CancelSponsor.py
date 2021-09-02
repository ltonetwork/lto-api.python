import base58
from PyCLTO import crypto
import struct
from PyCLTO.Transaction import Transaction


class CancelSponsor(Transaction):
    DEFAULT_SPONSOR_FEE = 500000000
    TYPE = 19

    def __init__(self, recipient):
        super().__init__()
        self.recipient = recipient
        crypto.validateAddress(recipient)
        self.txFee = self.DEFAULT_SPONSOR_FEE



    def toBinary(self):
        return (b'\x13' +
                b'\1' +
                crypto.str2bytes(crypto.getNetwork(self.sender)) +
                base58.b58decode(self.senderPublicKey) +
                base58.b58decode(self.recipient) +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.txFee))

    def toJson(self):
        return({
                "version": 1,
                "sender": self.sender,
                "senderPublicKey": self.senderPublicKey,
                "recipient": self.recipient,
                "fee": self.txFee,
                "timestamp": self.timestamp,
                "type": self.TYPE,
                "proofs": self.proofs
            })

    @staticmethod
    def fromData(data):
        tx = CancelSponsor(data['recipient'])
        tx.id = data['id']
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender']
        tx.senderPublicKey = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.recipient = data['recipient']
        tx.proofs = data['proofs']
        if 'height' in data:
            tx.height = data['height']
        return tx