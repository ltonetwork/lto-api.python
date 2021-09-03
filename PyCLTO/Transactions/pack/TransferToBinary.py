import base58
import struct
from PyCLTO import crypto

def toBinaryV2(transaction):
    return (b'\4' +
            b'\2' +
            base58.b58decode(transaction.senderPublicKey) +
            struct.pack(">Q", transaction.timestamp) +
            struct.pack(">Q", transaction.amount) +
            struct.pack(">Q", transaction.txFee) +
            base58.b58decode(transaction.recipient) +
            struct.pack(">H", len(transaction.attachment)) +
            crypto.str2bytes(transaction.attachment))


def toBinaryV3(transaction):
    return (b'\4' +
            b'\3' +
            crypto.str2bytes(transaction.chainId) +
            struct.pack(">Q", transaction.timestamp) +
            b'\1' +
            base58.b58decode(transaction.senderPublicKey) +
            struct.pack(">Q", transaction.txFee) +
            base58.b58decode(transaction.recipient) +
            struct.pack(">Q", transaction.amount) +
            struct.pack(">H", len(transaction.attachment)) +
            crypto.str2bytes(transaction.attachment))