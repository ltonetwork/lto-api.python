import base64
import json
import base58
from PyCLTO import crypto
import struct
import logging
from time import time
from PyCLTO.Transaction import Transaction
from PyCLTO.Account import Account


class setScript(Transaction):

    def __init__(self, txFee=0, timestamp=0):
        super().__init__()

        self.txFee = txFee
        self.timestamp = timestamp
        self.signature = ''
        self.publicKey = ''
        self.script = ''

        if self.txFee == 0:
            self.txFee = Transaction.DEFAULT_SCRIPT_FEE



    def signWith(self, script, account: Account):

        if self.timestamp == 0:
            self.timestamp = int(time() * 1000)

        self.script = script
        compiledScript = base64.b64decode(script)
        
        self.publicKey = account.publicKey

        sData = b'\13' + \
                b'\1' + \
                crypto.str2bytes(Transaction.getNetwork(account.address)) + \
                base58.b58decode(self.publicKey) + \
                b'\1' + \
                struct.pack(">H", len(compiledScript)) + \
                compiledScript + \
                struct.pack(">Q", self.txFee) + \
                struct.pack(">Q", self.timestamp)
        self.signature = account.sign(sData)

    def toJson(self):
        return ({
            "type": 13,
            "version": 1,
            "senderPublicKey": self.publicKey,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "script": 'base64:' + self.script,
            "proofs": [
                self.signature
            ]
        })

