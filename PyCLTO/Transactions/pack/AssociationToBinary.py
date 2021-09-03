import base58
import struct
from PyCLTO import crypto


def toBinaryV1(self):
    return (b'\x10' +
            b'\1' +
            crypto.str2bytes(crypto.getNetwork(self.sender)) +
            base58.b58decode(self.senderPublicKey) +
            base58.b58decode(self.recipient) +
            struct.pack(">i", self.associationType) +
            b'\1' +
            struct.pack(">H", len(crypto.str2bytes(self.anchor))) +
            crypto.str2bytes(self.anchor) +
            struct.pack(">Q", self.timestamp) +
            struct.pack(">Q", self.txFee))


def toBinaryV3(self):
    return (b'\x10' +
            b'\3' +
            crypto.str2bytes(self.chainId) +
            struct.pack(">Q", self.timestamp) +
            b'\1' +
            base58.b58decode(self.senderPublicKey) +
            struct.pack(">Q", self.txFee) +
            base58.b58decode(self.recipient) +
            struct.pack(">i", self.associationType) +
            crypto.str2bytes(crypto.getNetwork(self.sender)) +
            struct.pack(">Q", self.expires) +
            struct.pack(">H", len(crypto.str2bytes(self.anchor))) +
            crypto.str2bytes(self.anchor))