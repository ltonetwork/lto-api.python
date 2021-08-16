import base58
from PyCLTO import crypto
import struct
from time import time
from PyCLTO.Transaction import Transaction
from PyCLTO.Account import Account


class association(Transaction):
    def __init__(self, party, type, anchor, txFee=0, timestamp=0):
        super().__init__()

        self.txFee = txFee
        self.timestamp = timestamp
        self.party = party
        self.type = type
        self.anchor = anchor
        self.publicKey = ''
        self.signature = ''

        if self.txFee == 0:
            self.txFee = Transaction.DEFAULT_LEASE_FEE

    def signWith(self, account: Account):
        if self.timestamp == 0:
            self.timestamp = int(time() * 1000)
        self.publicKey = account.publicKey
        sData = b'\x10' + \
                b'\1' + \
                crypto.str2bytes(Transaction.getNetwork(account.address)) + \
                base58.b58decode(self.publicKey) + \
                base58.b58decode(self.party.address) + \
                struct.pack(">i", self.type) + \
                b'\1' + \
                struct.pack(">H", len(crypto.str2bytes(self.anchor))) + \
                crypto.str2bytes(self.anchor) + \
                struct.pack(">Q", self.timestamp) + \
                struct.pack(">Q", self.txFee)
        self.signature = account.sign(sData)

    def toJson(self):
        return ({
                "type": 16,
                "version": 1,
                "senderPublicKey": self.publicKey,
                "party": self.party.address,
                "associationType": self.type,
                "hash": base58.b58encode(crypto.str2bytes(self.anchor)),
                "fee": self.txFee,
                "timestamp": self.timestamp,
                "proofs": [
                    self.signature
                ]
            })
