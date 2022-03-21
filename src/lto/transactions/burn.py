import base58
import struct
from lto import crypto
from lto.transaction import Transaction


class Burn(Transaction):
    TYPE = 15
    DEFAULT_FEE = 100000000
    DEFAULT_VERSION = 3

    def __init__(self, amount):
        super().__init__()
        if amount < 1:
            raise Exception("Minimum burn amount = 1")
        self.amount = amount
        self.version = self.DEFAULT_VERSION
        self.tx_fee = self.DEFAULT_FEE

    def __to_binary_v3(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">Q", self.amount))

    def to_binary(self):
        if self.version == 3:
            return self.__to_binary_v3()
        else:
            raise Exception('Incorrect Version')

    def to_json(self):
        return (crypto.merge_dicts({
            "type": self.TYPE,
            "version": self.version,
            "id": self.id if self.id else "",
            "sender": self.sender,
            "senderKeyType": self.sender_key_type,
            "senderPublicKey": self.sender_public_key,
            "fee": self.tx_fee,
            "timestamp": self.timestamp,
            "amount": self.amount,
            "proofs": self.proofs,
            "height": self.height if self.height else ""
        }, self._sponsor_json()))

    @staticmethod
    def from_data(data):
        tx = Burn(data['amount'])
        tx.type = data['type']
        tx.version = data['version']
        tx.id = data['id'] if 'id' in data else ''
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.sender_key_type = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.sender_public_key = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.amount = data['amount']
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.height = data['height'] if 'height' in data else ''

        if "sponsor_public_key" in data:
            tx.sponsor = data['sponsor']
            tx.sponsor_public_key = data['sponsorPublicKey']
            tx.sponsor_key_type = data['sponsorKeyType']

        return tx
