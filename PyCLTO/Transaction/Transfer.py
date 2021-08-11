import json
import base58
from PyCLTO import crypto
import struct
import logging
from PyCLTO import PublicNode
from datetime import time

def transfer(self, recipient, amount, attachment='', txFee=0, timestamp=0):
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
        if txFee == 0:
            txFee = self.pyclto.DEFAULT_TX_FEE
        if timestamp == 0:
            timestamp = int(time.time() * 1000)
        sData = b'\4' + \
                b'\2' + \
                base58.b58decode(self.publicKey) + \
                struct.pack(">Q", timestamp) + \
                struct.pack(">Q", amount) + \
                struct.pack(">Q", txFee) + \
                base58.b58decode(recipient.address) + \
                struct.pack(">H", len(attachment)) + \
                crypto.str2bytes(attachment)
        signature = self.sign(self.privateKey, sData)
        data = json.dumps({
            "type": 4,
            "version": 2,
            "senderPublicKey": self.publicKey,
            "recipient": recipient.address,
            "amount": amount,
            "fee": txFee,
            "timestamp": timestamp,
            "attachment": base58.b58encode(crypto.str2bytes(attachment)),
            "signature": signature,
            "proofs": [signature]
        })

        return PublicNode.broadcast(data)