import json
import base58
from PyCLTO import crypto
import struct
import logging
from PyCLTO import PublicNode
from datetime import time
from PyCLTO.account import pyAccount
from PyCLTO import PyCLTO

def transfer(account, recipient, amount, attachment='', txFee=0, timestamp=0):
    if not account.privateKey:
        msg = 'Private key required'
        logging.error(msg)
        PyCLTO("T").throw_error(msg)

    elif amount <= 0:
        msg = 'Amount must be > 0'
        logging.error(msg)
        PyCLTO("T").throw_error(msg)
    elif PublicNode("https://testnet.lto.network").balance(address=account.address) < amount + txFee:
        msg = 'Insufficient LTO balance'
        logging.error(msg)
        PyCLTO("T").throw_error(msg)

    else:
        if txFee == 0:
            txFee = PyCLTO("T").DEFAULT_TX_FEE
        if timestamp == 0:
            timestamp = int(time.microsecond() * 1000)
        sData = b'\4' + \
                b'\2' + \
                base58.b58decode(account.publicKey) + \
                struct.pack(">Q", timestamp) + \
                struct.pack(">Q", amount) + \
                struct.pack(">Q", txFee) + \
                base58.b58decode(recipient.address) + \
                struct.pack(">H", len(attachment)) + \
                crypto.str2bytes(attachment)
        signature = pyAccount.sign(account.privateKey, sData)
        data = json.dumps({
            "type": 4,
            "version": 2,
            "senderPublicKey": account.publicKey,
            "recipient": recipient.address,
            "amount": amount,
            "fee": txFee,
            "timestamp": timestamp,
            "attachment": base58.b58encode(crypto.str2bytes(attachment)),
            "signature": signature,
            "proofs": [signature]
        })

        return PublicNode.broadcast(data)