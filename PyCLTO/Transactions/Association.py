import base58
from PyCLTO import crypto
import struct
from time import time
from PyCLTO.Transaction import Transaction
from PyCLTO.Account import Account


class Association(Transaction):
    DEFAULT_LEASE_FEE = 100000000
    TYPE = 16

    def __init__(self, party, associationType, anchor=''):
        super().__init__()
        self.party = party
        self.associationType = associationType
        self.anchor = anchor
        self.txFee = self.DEFAULT_LEASE_FEE


    def toBinary(self):
        return (b'\x10' +
                b'\1' +
                crypto.str2bytes(crypto.getNetwork(self.sender)) +
                base58.b58decode(self.senderPublicKey) +
                base58.b58decode(self.party) +
                struct.pack(">i", self.associationType) +
                b'\1' +
                struct.pack(">H", len(crypto.str2bytes(self.anchor))) +
                crypto.str2bytes(self.anchor) +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.txFee))


    def toJson(self):
        return ({
                "type": self.TYPE,
                "version": 1,
                "senderPublicKey": self.senderPublicKey,
                "party": self.party,
                "associationType": self.associationType,
                "hash": base58.b58encode(crypto.str2bytes(self.anchor)),
                "fee": self.txFee,
                "timestamp": self.timestamp,
                "proofs": self.proofs
            })

