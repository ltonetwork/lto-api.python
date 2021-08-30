import json
import base58
from PyCLTO import crypto
import struct
import logging
from time import time
from PyCLTO.Transaction import Transaction
from PyCLTO.Account import Account

class Lease(Transaction):
    DEFAULT_LEASE_FEE = 100000000
    TYPE = 8

    def __init__(self, recipient, amount):
        super().__init__()
        self.amount = amount
        self.recipient = recipient
        crypto.validateAddress(address)
        self.txFee = self.DEFAULT_LEASE_FEE

        if self.amount <= 0:
            raise Exception ('Amount must be > 0')


    def toBinary(self):
        return (b'\x08' +
                b'\2' +
                b'\0' +
                base58.b58decode(self.senderPublicKey) +
                base58.b58decode(self.recipient) +
                struct.pack(">Q", self.amount) +
                struct.pack(">Q", self.txFee) +
                struct.pack(">Q", self.timestamp))

    def toJson(self):
        return ({
            "version": 2,
            "senderPublicKey": self.senderPublicKey,
            "recipient": self.recipient,
            "amount": self.amount,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "type": self.TYPE,
            "proofs": self. proofs
        })
