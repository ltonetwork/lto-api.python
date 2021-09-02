import base64
import json
import base58
from PyCLTO import crypto
import struct
import logging
from time import time
from PyCLTO.Transaction import Transaction
from PyCLTO.Account import Account


class SetScript(Transaction):
    TYPE = 13
    DEFAULT_SCRIPT_FEE = 500000000

    def __init__(self, script):
        super().__init__()

        self.script = script
        self.compiledScript = base64.b64decode(self.script)

        self.txFee = self.DEFAULT_SCRIPT_FEE


    def toBinary(self):
        return (b'\13' +
                b'\1' +
                crypto.str2bytes(crypto.getNetwork(self.sender)) +
                base58.b58decode(self.senderPublicKey) +
                b'\1' +
                struct.pack(">H", len(self.compiledScript)) +
                self.compiledScript +
                struct.pack(">Q", self.txFee) +
                struct.pack(">Q", self.timestamp))

    def toJson(self):
        return ({
            "type": self.TYPE,
            "version": 1,
            "sender": self.sender,
            "senderPublicKey": self.senderPublicKey,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "script": 'base64:' + str(self.script),
            "proofs": self.proofs
        })

    @staticmethod
    def fromData(data):
        tx = SetScript(data['script'])
        tx.id = data['id']
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender']
        tx.senderPublicKey = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.proofs = data['proofs']
        tx.script = data['script']
        if 'height' in data:
            tx.height = data['height']
        return tx