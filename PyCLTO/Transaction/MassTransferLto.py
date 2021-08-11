import json
import base58
from PyCLTO import crypto
import struct
import logging
from datetime import time

def massTransferLTO(self, transfers, attachment='', timestamp=0, baseFee=0):
    if baseFee == 0:
        baseFee = self.pyclto.DEFAULT_BASE_FEE

    txFee = baseFee + int(len(transfers) * baseFee / 10)
    totalAmount = 0

    for i in range(0, len(transfers)):
        totalAmount += transfers[i]['amount']

    if not self.privateKey:
        msg = 'Private key required'
        logging.error(msg)
        self.pyclto.throw_error(msg)
    elif len(transfers) > 100:
        msg = 'Too many recipients'
        logging.error(msg)
        self.pyclto.throw_error(msg)
    elif not self.pyclto.OFFLINE and self.balance() < totalAmount + txFee:
        msg = 'Insufficient LTO balance'
        logging.error(msg)
        self.pyclto.throw_error(msg)
    else:
        if timestamp == 0:
            timestamp = int(time.time() * 1000)
        transfersData = b''
        for i in range(0, len(transfers)):
            transfersData += base58.b58decode(transfers[i]['recipient']) + struct.pack(">Q", transfers[i]['amount'])
        sData = b'\x0b' + \
                b'\1' + \
                base58.b58decode(self.publicKey) + \
                struct.pack(">H", len(transfers)) + \
                transfersData + \
                struct.pack(">Q", timestamp) + \
                struct.pack(">Q", txFee) + \
                struct.pack(">H", len(attachment)) + \
                crypto.str2bytes(attachment)

        signature = self.sign(self.privateKey, sData)

        data = json.dumps({
            "type": 11,
            "version": 1,
            "senderPublicKey": self.publicKey,
            "fee": txFee,
            "timestamp": timestamp,
            "transfers": transfers,
            "attachment": base58.b58encode(crypto.str2bytes(attachment)),
            "signature": signature,
            "proofs": [
                signature
            ]
        })

        return self.pyclto.wrapper('/transactions/broadcast', data)