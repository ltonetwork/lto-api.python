import json
import base58
import struct
from time import time
from PyCLTO.Transaction import Transaction
from PyCLTO.Account import Account


class CancelLease(Transaction):
    TYPE = 9
    DEFAULT_LEASE_FEE = 100000000

    def __init__(self, leaseId):
        super().__init__()
        self.leaseId= leaseId
        self.txFee = self.DEFAULT_LEASE_FEE



    def toBinary(self):
        return (b'\x09' +
                base58.b58decode(self.senderPublicKey) +
                struct.pack(">Q", self.txFee) +
                struct.pack(">Q", self.timestamp) +
                base58.b58decode(self.leaseId))

    def toJson(self):
        return({
            "senderPublicKey": self.senderPublicKey,
            "txId": self.leaseId,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "signature": self.proofs,
            "type": self.TYPE
        })


