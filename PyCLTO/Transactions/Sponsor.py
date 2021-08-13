import base58
from PyCLTO import crypto
import struct
from time import time
from PyCLTO.Account import Account
from PyCLTO.Transaction import Transaction
from PyCLTO import PyCLTO

class Sponsor(Transaction):
    def __init__(self, recipient, txFee=0, timestamp=0):
        super().__init__()
        self.recipient = recipient
        self.txFee = txFee
        self.timestamp = timestamp
        self.signature = ''
        self.senderPublickKey = ''

        if self.txFee == 0:
            self.txFee = Transaction.DEFAULT_SPONSOR_FEE

    def signWith(self, account: Account):
        if self.timestamp == 0:
            self.timestamp = int(time() * 1000)

        self.senderPublickKey = account.getPublicKey(account.publicKey)


        # have to correct the Chain_ID because it's just creating an object and taking the basic one,
        # where should the Chain_ID be taken from ??
        sData = b'\x12' + \
                b'\1' + \
                crypto.str2bytes(str(PyCLTO().CHAIN_ID)) + \
                base58.b58decode(self.senderPublickKey) + \
                base58.b58decode(self.recipient.address) + \
                struct.pack(">Q", self.timestamp) + \
                struct.pack(">Q", self.txFee)

        self.signature = account.sign(sData)

    def toJson(self):
        return ({
            "version": 1,
            "senderPublicKey": self.senderPublickKey,
            "recipient": self.recipient.address,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "type": 18,
            "proofs": [self.signature]
        })
