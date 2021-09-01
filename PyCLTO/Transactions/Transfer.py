import base58
import struct
import PyCLTO
import PyCLTO.crypto
from PyCLTO.Transaction import Transaction


class Transfer(Transaction):
    TYPE = 4
    DEFAULT_TX_FEE = 100000000

    def __init__(self, recipient, amount, attachment=''):
        super().__init__()
        self.recipient = recipient
        PyCLTO.crypto.validateAddress(recipient)
        self.amount = amount
        self.attachment = attachment

        if self.amount <= 0:
            raise Exception('Amount should be positive')

        self.txFee = self.DEFAULT_TX_FEE


    def toBinary(self):
        return (b'\4' +
                b'\2' +
                base58.b58decode(self.senderPublicKey) +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.amount) +
                struct.pack(">Q", self.txFee) +
                base58.b58decode(self.recipient) +
                struct.pack(">H", len(self.attachment)) +
                PyCLTO.crypto.str2bytes(self.attachment))


    def toJson(self):
        return ({
            "type": self.TYPE,
            "version": 2,
            "senderPublicKey": self.senderPublicKey,
            "recipient": self.recipient,
            "amount": self.amount,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "attachment": base58.b58encode(PyCLTO.crypto.str2bytes(self.attachment)),
            "proofs": self.proofs
        })

    @staticmethod
    def fromData(data):
        tx = Transfer(data['recipient'], data['amount'], data['attachment'])
        tx.id = data['id']
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender']
        tx.senderPublicKey = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.amount = data['amount']
        tx.recipient = data['recipient']
        tx.attachment = data['attachment']
        tx.proofs = data['proofs']
        tx.height = data['height']
        return tx