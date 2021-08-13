import json
import base58
from PyCLTO import crypto
import struct
import logging
from time import time
from PyCLTO.Account import Account


class Transfer(object):
    DEFAULT_TX_FEE = 100000000

    def __init__(self, recipient, amount, attachment='', txFee=0, timestamp=0):
        self.recipient = recipient
        self.timestamp = 0
        self.signature = ''
        self.txFee = txFee
        self.amount = amount
        self.attachment = attachment
        self.timestamp = timestamp
        self.senderPublicKey = ''

        if self.amount <= 0:
            raise Exception('Amount should be positive')

        if self.txFee == 0:
            self.txFee = self.DEFAULT_TX_FEE

    def signWith(self, account: Account):
        if self.timestamp == 0:
            self.timestamp = int(time() * 1000)

        sData = b'\4' + \
                b'\2' + \
                bytes(account.publicKey) + \
                struct.pack(">Q", self.timestamp) + \
                struct.pack(">Q", self.amount) + \
                struct.pack(">Q", self.txFee) + \
                base58.b58decode(self.recipient.address) + \
                struct.pack(">H", len(self.attachment)) + \
                crypto.str2bytes(self.attachment)


        #self.senderPublicKey = base58.b58encode(bytes(account.publicKey))
        self.senderPublicKey = account.getPublicKey(account.publicKey)
        self.signature = account.sign(message=sData)

    def toJson(self):
        return ({
            "type": 4,
            "version": 2,
            "senderPublicKey": self.senderPublicKey,
            "recipient": self.recipient.address,
            "amount": self.amount,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "attachment": base58.b58encode(crypto.str2bytes(self.attachment)),
            "proofs": [self.signature]
        })