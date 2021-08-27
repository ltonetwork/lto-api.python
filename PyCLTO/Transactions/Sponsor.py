import base58
from PyCLTO import crypto
import struct
from PyCLTO.Transaction import Transaction


class Sponsor(Transaction):
    TYPE = 18
    DEFAULT_SPONSOR_FEE = 500000000

    def __init__(self, recipient):
        super().__init__()
        self.recipient = recipient
        self.txFee = self.DEFAULT_SPONSOR_FEE

    def toBinary(self):
        return (b'\x12' + b'\1' +
                crypto.str2bytes(crypto.getNetwork(self.sender)) +
                base58.b58decode(self.senderPublicKey)
                + base58.b58decode(self.recipient)
                + struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.txFee))


    def toJson(self):
        return ({
            "type": self.TYPE,
            "version": 1,
            "recipient": self.recipient,
            "sender": self.sender,
            "senderPublicKey": self.senderPublicKey,
            "timestamp": self.timestamp,
            "fee": self.txFee,
            "proofs": self.proofs
        })
