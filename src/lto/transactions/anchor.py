import base58
from lto import crypto
from lto.binary import Binary
from lto.transaction import Transaction
import struct


class Anchor(Transaction):
    TYPE = 15
    BASE_FEE = 25000000
    VAR_FEE = 10000000
    DEFAULT_VERSION = 3

    def __init__(self, *anchors: bytes):
        super().__init__()

        self.anchors = [Binary(anchor) for anchor in anchors]
        self.tx_fee = self.BASE_FEE + len(anchors) * self.VAR_FEE
        self.version = self.DEFAULT_VERSION

    def __anchors_to_binary(self):
        return b''.join(struct.pack(">H", len(anchor)) + anchor for anchor in self.anchors)

    def __to_binary_v1(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\1' +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">H", len(self.anchors)) +
                self.__anchors_to_binary() +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.tx_fee))

    def __to_binary_v3(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">H", len(self.anchors)) +
                self.__anchors_to_binary())

    def to_binary(self):
        if self.version == 1:
            return self.__to_binary_v1()
        elif self.version == 3:
            return self.__to_binary_v3()
        else:
            raise Exception('Incorrect Version')

    def to_json(self):
        return crypto.clean_dict({
                "id": self.id,
                "type": self.TYPE,
                "version": self.version,
                "sender": self.sender,
                "senderKeyType": self.sender_key_type,
                "senderPublicKey": self.sender_public_key,
                "fee": self.tx_fee,
                "timestamp": self.timestamp,
                "anchors": [anchor.base58() for anchor in self.anchors],
                "sponsor": self.sponsor,
                "sponsorKeyType": self.sponsor_key_type,
                "sponsorPublicKey": self.sponsor_public_key,
                "proofs": self.proofs or None,
                "height": self.height
            })

    @staticmethod
    def from_data(data):
        tx = Anchor(*map(lambda anchor: Binary.frombase58(anchor), data.get('anchors', [])))
        tx._init_from_data(data)

        return tx
