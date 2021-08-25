import json
import base58
from PyCLTO import crypto
import struct
import logging
from time import time
from PyCLTO.Transaction import Transaction
from PyCLTO.Account import Account


class MassTransferLTO(Transaction):
    DEFAULT_BASE_FEE = 100000000
    TYPE = 11

    def __init__(self, transfers, attachment='', baseFee=0):
        super().__init__()
        self.baseFee = baseFee
        self.transfers = transfers
        self.totalAmount = 0
        self.attachment = attachment
        self.transfersData = ''

        self.baseFee = self.DEFAULT_BASE_FEE

        self.txFee = self.baseFee + int(len(self.transfers) * self.baseFee / 10)

        for i in range(0, len(self.transfers)):
            self.totalAmount += self.transfers[i]['amount']

        if len(self.transfers) > 100:
            raise Exception('Too many recipients')

        self.transfersData = b''
        for i in range(0, len(self.transfers)):
            self.transfersData += base58.b58decode(self.transfers[i]['recipient']) \
                             + struct.pack(">Q", self.transfers[i]['amount'])
    def toBinary(self):
        return (b'\x0b' +
                b'\1' +
                base58.b58decode(self.senderPublicKey) +
                struct.pack(">H", len(self.transfers)) +
                self.transfersData +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.txFee) +
                struct.pack(">H", len(self.attachment)) +
                crypto.str2bytes(self.attachment))


    def toJson(self):
        return ({
            "type": self.TYPE,
            "version": 1,
            "senderPublicKey": self.senderPublicKey,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "transfers": self.transfers,
            "attachment": base58.b58encode(crypto.str2bytes(self.attachment)),
            "proofs": self.proofs
        })

