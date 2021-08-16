import json
import base58
from PyCLTO import crypto
import struct
import logging
from time import time
from PyCLTO.Transaction import Transaction
from PyCLTO.Account import Account


class MassTransferLTO(Transaction):
    def __init__(self, transfers, attachment='', timestamp=0, baseFee=0):
        super().__init__()
        self.baseFee = baseFee
        self.timestamp = timestamp
        self.txFee = ''
        self.signature = ''
        self.transfers = transfers
        self.publicKey = ''
        self.totalAmount = 0
        self.attachment = ''

        if self.baseFee == 0:
            self.baseFee = Transaction.DEFAULT_BASE_FEE

        self.txFee = self.baseFee + int(len(self.transfers) * self.baseFee / 10)

        for i in range(0, len(self.transfers)):
            self.totalAmount += self.transfers[i]['amount']

        if len(self.transfers) > 100:
            raise Exception('Too many recipients')

        if self.timestamp == 0:
            self.timestamp = int(time() * 1000)


    def signWith(self, account: Account):
        self.publicKey = account.publicKey
        transfersData = b''
        for i in range(0, len(self.transfers)):
            transfersData += base58.b58decode(self.transfers[i]['recipient']) \
                             + struct.pack(">Q", self.transfers[i]['amount'])
        sData = b'\x0b' + \
                b'\1' + \
                base58.b58decode(self.publicKey) + \
                struct.pack(">H", len(self.transfers)) + \
                transfersData + \
                struct.pack(">Q", self.timestamp) + \
                struct.pack(">Q", self.txFee) + \
                struct.pack(">H", len(self.attachment)) + \
                crypto.str2bytes(self.attachment)
        self.signature = account.sign(sData)


    def toJson(self):
        return ({
            "type": 11,
            "version": 1,
            "senderPublicKey": self.publicKey,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "transfers": self.transfers,
            "attachment": base58.b58encode(crypto.str2bytes(self.attachment)),
            "proofs": [
                self.signature
            ]
        })

