import json
import base58
from PyCLTO import crypto
import struct
import logging
from datetime import time

def lease(self, recipient, amount, txFee=0, timestamp=0):
    if txFee == 0:
        txFee = self.pyclto.DEFAULT_LEASE_FEE
    if not self.privateKey:
        msg = 'Private key required'
        logging.error(msg)
        self.pyclto.throw_error(msg)
    elif amount <= 0:
        msg = 'Amount must be > 0'
        logging.error(msg)
        self.pyclto.throw_error(msg)
    elif not self.pyclto.OFFLINE and self.balance() < amount + txFee:
        msg = 'Insufficient LTO balance'
        logging.error(msg)
        self.pyclto.throw_error(msg)
    else:
        if timestamp == 0:
            timestamp = int(time.time() * 1000)
        sData = b'\x08' + \
                b'\2' + \
                b'\0' + \
                base58.b58decode(self.publicKey) + \
                base58.b58decode(recipient.address) + \
                struct.pack(">Q", amount) + \
                struct.pack(">Q", txFee) + \
                struct.pack(">Q", timestamp)
        signature = self.sign(self.privateKey, sData)
        data = json.dumps({
            "version": 2,
            "senderPublicKey": self.publicKey,
            "recipient": recipient.address,
            "amount": amount,
            "fee": txFee,
            "timestamp": timestamp,
            "signature": signature,
            "type": 8,
            "proofs": [
                signature
            ]
        })
        req = self.pyclto.wrapper('/transactions/broadcast', data)
        return req