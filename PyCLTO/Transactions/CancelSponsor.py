import json
import base58
from PyCLTO import crypto
import struct
import logging
from time import time
from PyCLTO.Transaction import Transaction
from PyCLTO.Account import Account


class CancelSponsor(Transaction):
    def __init__(self, recipient, txFee=0, timestamp=0):
        super().__init__()

        self.recipient = recipient
        self.txFee = txFee
        self.timestamp = timestamp
        self.signature = ''
        self.publicKey = ''

        if self.txFee == 0:
            self.txFee = Transaction.DEFAULT_SPONSOR_FEE


    def signWith(self, account: Account):
        if self.timestamp == 0:
            self.timestamp = int(time() * 1000)
        self.publicKey = account.publicKey
        sData = b'\x13' + \
                b'\1' + \
                crypto.str2bytes(Transaction.getNetwork(account.address)) + \
                base58.b58decode(self.publicKey) + \
                base58.b58decode(self.recipient.address) + \
                struct.pack(">Q", self.timestamp) + \
                struct.pack(">Q", self.txFee)
        self.signature = account.sign(sData)

    def toJson(self):
        return({
                "version": 1,
                "senderPublicKey": self.publicKey,
                "recipient": self.recipient.address,
                "fee": self.txFee,
                "timestamp": self.timestamp,
                "type": 19,
                "proofs": [
                    self.signature
                ]
            })
