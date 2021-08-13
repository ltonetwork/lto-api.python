import json
import base58
from PyCLTO import crypto
import struct
import logging
from datetime import time


def anchor(self, anchor, txFee=0, timestamp=0):
    if txFee == 0:
        txFee = self.pyclto.DEFAULT_LEASE_FEE
    if not self.privateKey:
        msg = 'Private key required'
        logging.error(msg)
        self.pyclto.throw_error(msg)

    elif not self.pyclto.OFFLINE and self.balance() < txFee:
        msg = 'Insufficient LTO balance'
        logging.error(msg)
        self.pyclto.throw_error(msg)
    else:
        if timestamp == 0:
            timestamp = int(time.time() * 1000)
        sData = b'\x0f' + \
                b'\1' + \
                base58.b58decode(self.publicKey) + \
                struct.pack(">H", 1) + \
                struct.pack(">H", len(crypto.str2bytes(anchor))) + \
                crypto.str2bytes(anchor) + \
                struct.pack(">Q", timestamp) + \
                struct.pack(">Q", txFee)
        signature = self.sign(self.privateKey, sData)
        data = json.dumps({
            "type": 15,
            "version": 1,
            "senderPublicKey": self.publicKey,
            "anchors": [
                base58.b58encode(crypto.str2bytes(anchor))
            ],
            "fee": txFee,
            "timestamp": timestamp,
            "proofs": [
                signature
            ]
        })
        req = self.pyclto.wrapper('/transactions/broadcast', data)
        return req