import base58
from lto import crypto
from lto.binary import Binary
from lto.transaction import Transaction
import struct


class MappedAnchor(Transaction):
    TYPE = 22
    BASE_FEE = 25000000
    VAR_FEE = 10000000
    DEFAULT_VERSION = 3

    def __init__(self, anchors: dict):
        super().__init__()

        self.anchors = {Binary(k): Binary(v) for k, v in anchors.items()}
        self.tx_fee = self.BASE_FEE + len(anchors) * self.VAR_FEE
        self.version = self.DEFAULT_VERSION

    def __anchors_to_binary(self):
        return b''.join(struct.pack(">H", len(k)) + k + struct.pack(">H", len(v)) + v for k, v in self.anchors.items())


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
        if self.version == 3:
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
                "anchors": {k.base58(): v.base58() for k, v in self.anchors.items()},
                "sponsor": self.sponsor,
                "sponsorKeyType": self.sponsor_key_type,
                "sponsorPublicKey": self.sponsor_public_key,
                "proofs": self.proofs or None,
                "height": self.height
            })

    @staticmethod
    def from_data(data):
        tx = MappedAnchor({Binary.frombase58(k): Binary.frombase58(v) for k, v in data.get('anchors', {}).items()})
        tx._init_from_data(data)

        return tx
