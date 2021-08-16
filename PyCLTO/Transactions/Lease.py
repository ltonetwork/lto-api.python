import json
import base58
from PyCLTO import crypto
import struct
import logging
from time import time
from PyCLTO.Transaction import Transaction
from PyCLTO.Account import Account

class lease(Transaction):
    def __init__(self, recipient, amount, txFee=0, timestamp=0):
        super().__init__()

        self.txFee = txFee
        self.timestamp = timestamp
        self.signature = ''
        self.amount = amount
        self.publicKey = ''
        self.recipient = recipient
        self.signature = ''

        if self.txFee == 0:
            self.txFee = Transaction.DEFAULT_LEASE_FEE

        if self.amount <= 0:
            raise Exception ('Amount must be > 0')

    def SignWith(self, account: Account):
        if self.timestamp == 0:
            self.timestamp = int(time() * 1000)
        self.publicKey = account.publicKey
        sData = b'\x08' + \
                b'\2' + \
                b'\0' + \
                base58.b58decode(self.publicKey) + \
                base58.b58decode(self.recipient.address) + \
                struct.pack(">Q", self.amount) + \
                struct.pack(">Q", self.txFee) + \
                struct.pack(">Q", self.timestamp)
        self.signature = account.sign(sData)

    def toJson(self):
        return ({
            "version": 2,
            "senderPublicKey": self.publicKey,
            "recipient": self.recipient.address,
            "amount": self.amount,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "type": 8,
            "proofs": [
               self. signature
            ]
        })
