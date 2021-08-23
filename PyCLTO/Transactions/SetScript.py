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
            "senderPublicKey": self.senderPublicKey,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "script": 'base64:' + self.script,
            "proofs": [
                self.signature
            ]
        })

