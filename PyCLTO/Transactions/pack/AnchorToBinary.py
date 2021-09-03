import base58
import struct
from PyCLTO import crypto


def toBinaryV1(self):
    return (b'\x0f' +
            b'\1' +
            base58.b58decode(self.senderPublicKey) +
            struct.pack(">H", 1) +
            struct.pack(">H", len(crypto.str2bytes(self.anchor))) +
            crypto.str2bytes(self.anchor) +
            struct.pack(">Q", self.timestamp) +
            struct.pack(">Q", self.txFee))


def toBinaryV3(self):
    return (
            b'\x0f' +
            b'\1' +
            crypto.str2bytes(self.chainId) +
            struct.pack(">Q", self.timestamp) +
            b'\1' +
            base58.b58decode(self.senderPublicKey) +
            struct.pack(">Q", self.txFee) +
            struct.pack(">H", 1) +
            struct.pack(">H", len(crypto.str2bytes(self.anchor))) +
            crypto.str2bytes(self.anchor)
    )