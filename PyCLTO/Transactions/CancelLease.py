import json
import base58
import struct
from time import time
from PyCLTO.Transaction import Transaction
from PyCLTO.Account import Account


class CancelLease(Transaction):
    def __init__(self, leaseId, txFee=0, timestamp=0):
        super().__init__()
        self.txFee = txFee
        self.timestamp = timestamp
        self.signature = ''
        self.publicKey = ''
        self.leaseId= leaseId

        if self.txFee == 0:
            self.txFee = Transaction.DEFAULT_LEASE_FEE


    def signWith(self, account: Account):
        self.publicKey = account.publicKey
        if self.timestamp == 0:
            self.timestamp = int(time() * 1000)
        sData = b'\x09' + \
                base58.b58decode(self.publicKey) + \
                struct.pack(">Q", self.txFee) + \
                struct.pack(">Q", self.timestamp) + \
                base58.b58decode(self.leaseId)
        self.signature = account.sign(sData)

    def toJson(self):
        return({
            "senderPublicKey": self.publicKey,
            "txId": self.leaseId,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "type": 9
        })


