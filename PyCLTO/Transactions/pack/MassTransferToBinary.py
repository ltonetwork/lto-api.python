import base58
import struct
from PyCLTO import crypto


def toBinaryV1(self):
    return (b'\x0b' +
            b'\1' +
            base58.b58decode(self.senderPublicKey) +
            struct.pack(">H", len(self.transfers)) +
            self.transfersData +
            struct.pack(">Q", self.timestamp) +
            struct.pack(">Q", self.txFee) +
            struct.pack(">H", len(self.attachment)) +
            crypto.str2bytes(self.attachment))


def toBinaryV3(self):
    return (
            b'\x0b' +
            b'\3' +
            crypto.str2bytes(self.chainId) +
            struct.pack(">Q", self.timestamp) +
            b'\1' +
            base58.b58decode(self.senderPublicKey) +
            struct.pack(">Q", self.txFee) +
            struct.pack(">H", len(self.transfers)) +

            self.transfersData +

            struct.pack(">H", len(self.attachment)) +
            crypto.str2bytes(self.attachment))