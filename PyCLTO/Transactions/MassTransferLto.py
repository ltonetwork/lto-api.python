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

    def __init__(self, transfers, attachment=''):
        super().__init__()
        self.transfers = transfers
        self.attachment = attachment
        self.transfersData = ''
        self.baseFee = self.DEFAULT_BASE_FEE
        self.txFee = self.baseFee + int(len(self.transfers) * self.baseFee / 10)


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
            "sender": self.sender,
            "senderPublicKey": self.senderPublicKey,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "transfers": self.transfers,
            "attachment": base58.b58encode(crypto.str2bytes(self.attachment)),
            "proofs": self.proofs
        })

    @staticmethod
    def fromData(data):
        tx = MassTransferLTO(transfers='')
        tx.id = data['id']
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender']
        tx.senderPublicKey = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.attachment = data['attachment']
        tx.proofs = data['proofs']
        tx.transfers = data['transfers']
        return tx

