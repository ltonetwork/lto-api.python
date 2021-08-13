import json
import base58
from PyCLTO import crypto
import struct
import logging
from datetime import time

def revokeAssociation(self, party, type, anchor, txFee=0, timestamp=0):
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
        sData = b'\x11' + \
                b'\1' + \
                crypto.str2bytes(str(self.pyclto.CHAIN_ID)) + \
                base58.b58decode(self.publicKey) + \
                base58.b58decode(party.address) + \
                struct.pack(">i", type) + \
                b'\1' + \
                struct.pack(">H", len(crypto.str2bytes(anchor))) + \
                crypto.str2bytes(anchor) + \
                struct.pack(">Q", timestamp) + \
                struct.pack(">Q", txFee)

        signature = self.sign(self.privateKey, sData)
        data = json.dumps({
            "type": 17,
            "version": 1,
            "senderPublicKey": self.publicKey,
            "party": party.address,
            "associationType": type,
            "hash": base58.b58encode(crypto.str2bytes(anchor)),
            "fee": txFee,
            "timestamp": timestamp,
            "proofs": [
                signature
            ]
        })
        req = self.pyclto.wrapper('/transactions/broadcast', data)
        return req