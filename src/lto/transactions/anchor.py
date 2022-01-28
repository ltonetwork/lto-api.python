import base58
from lto import crypto
from lto.transaction import Transaction
import struct


class Anchor(Transaction):
    TYPE = 15
    BASE_FEE = 25000000
    VAR_FEE = 10000000
    DEFAULT_VERSION = 3

    def __init__(self, *anchors):
        super().__init__()

        self.anchors = anchors
        self.tx_fee = self.BASE_FEE + len(anchors) * self.VAR_FEE
        self.version = self.DEFAULT_VERSION

    def __anchors_to_binary(self):
        binary = b''
        for anchor in self.anchors:
            binary += struct.pack(">H", len(crypto.str2bytes(anchor)))
            binary += crypto.str2bytes(anchor)

        return binary

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
        return (crypto.merge_dicts(
            {
                "id": self.id if self.id else "",
                "type": self.TYPE,
                "version": self.version,
                "sender": self.sender,
                "senderKeyType": self.sender_key_type,
                "senderPublicKey": self.sender_public_key,
                "fee": self.tx_fee,
                "timestamp": self.timestamp,
                "anchors": list(map(lambda anchor: base58.b58encode(crypto.str2bytes(anchor)), self.anchors)),
                "proofs": self.proofs,
                "height": self.height if self.height else ""
            },
            self._sponsor_json()))

    @staticmethod
    def from_data(data):
        tx = Anchor("")
        tx.id = data['id'] if 'id' in data else ''
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.sender_key_type = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.sender_public_key = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.anchors = data['anchors']
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.height = data['height'] if 'height' in data else ''

        if "sponsor_public_key" in data:
            tx.sponsor = data['sponsor']
            tx.sponsor_public_key = data['sponsorPublicKey']
            tx.sponsor_key_type = data['sponsorKeyType']

        return tx
