import json
from abc import ABC

import base58
from PyCLTO import crypto
import struct
import logging
from time import time
from PyCLTO.Account import Account
from PyCLTO.Transaction import Transaction


class Transfer(Transaction):
    TYPE = 4
    DEFAULT_TX_FEE = 100000000

    def __init__(self, recipientAddress, amount, attachment=''):
        super().__init__()
        self.recipient = recipientAddress
        self.amount = amount
        self.attachment = attachment

        if self.amount <= 0:
            raise Exception('Amount should be positive')

        self.txFee = self.DEFAULT_TX_FEE


    def toBinary(self):
        return (b'\4' +
                b'\2' +
                base58.b58decode(self.senderPublicKey) +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.amount) +
                struct.pack(">Q", self.txFee) +
                base58.b58decode(self.recipient) +
                struct.pack(">H", len(self.attachment)) +
                crypto.str2bytes(self.attachment))


    def toJson(self):
        return ({
            "type": self.TYPE,
            "version": 2,
            "senderPublicKey": self.senderPublicKey,
            "recipient": self.recipient,
            "amount": self.amount,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "attachment": base58.b58encode(crypto.str2bytes(self.attachment)),
            "proofs": self.proofs
        })