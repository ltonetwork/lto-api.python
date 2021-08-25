import json
import base58
from PyCLTO import crypto
import struct
import logging
from time import time
from PyCLTO.Transaction import Transaction
from PyCLTO.Account import Account


class CancelSponsor(Transaction):
    DEFAULT_SPONSOR_FEE = 500000000
    TYPE = 19

    def __init__(self, recipient):
        super().__init__()
        self.recipient = recipient
        self.txFee = Transaction.DEFAULT_SPONSOR_FEE



    def toBinary(self):
        return (b'\x13' +
                b'\1' +
                crypto.str2bytes(crypto.getNetwork(self.sender)) +
                base58.b58decode(self.senderPublicKey) +
                base58.b58decode(self.recipient.address) +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.txFee))

    def toJson(self):
        return({
                "version": 1,
                "senderPublicKey": self.senderPublicKey,
                "recipient": self.recipient.address,
                "fee": self.txFee,
                "timestamp": self.timestamp,
                "type": self.TYPE,
                "proofs": self.proofs
            })
