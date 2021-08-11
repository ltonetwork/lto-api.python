import json
import base58
from PyCLTO import crypto
import struct
import logging
from datetime import time

def cancelLease(self, leaseId, txFee=0, timestamp=0):
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
        sData = b'\x09' + \
                base58.b58decode(self.publicKey) + \
                struct.pack(">Q", txFee) + \
                struct.pack(">Q", timestamp) + \
                base58.b58decode(leaseId)
        signature = self.sign(self.privateKey, sData)
        data = json.dumps({
            "senderPublicKey": self.publicKey,
            "txId": leaseId,
            "fee": txFee,
            "timestamp": timestamp,
            "signature": signature,
            "type": 9
        })
        req = self.pyclto.wrapper('/transactions/broadcast', data)
        if self.pyclto.OFFLINE:
            return req
        elif 'leaseId' in req:
            return req['leaseId']