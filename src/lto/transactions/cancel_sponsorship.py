import base58
from lto import crypto
import struct
from lto.transaction import Transaction


class CancelSponsorship(Transaction):
    DEFAULT_FEE = 500000000
    TYPE = 19
    DEFAULT_VERSION = 3

    def __init__(self, recipient):
        super().__init__()
        self.recipient = recipient
        crypto.validate_address(recipient)
        self.tx_fee = self.DEFAULT_FEE
        self.version = self.DEFAULT_VERSION

    def __to_binary_v1(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\1' +
                crypto.str2bytes(crypto.get_network(self.sender)) +
                base58.b58decode(self.sender_public_key) +
                base58.b58decode(self.recipient) +
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
                base58.b58decode(self.recipient))

    def to_binary(self):
        if self.version == 1:
            return self.__to_binary_v1()
        elif self.version == 3:
            return self.__to_binary_v3()
        else:
            raise Exception('Incorrect Version')

    def to_json(self):
        return (crypto.merge_dicts({
            "id": self.id if self.id else "",
            "type": self.TYPE,
            "version": self.version,
            "senderKeyType": self.sender_key_type,
            "recipient": self.recipient,
            "sender": self.sender,
            "senderPublicKey": self.sender_public_key,
            "timestamp": self.timestamp,
            "fee": self.tx_fee,
            "proofs": self.proofs,
            "height": self.height if self.height else ""
        }, self._sponsor_json()))

    @staticmethod
    def from_data(data):
        tx = CancelSponsorship(data['recipient'])
        tx.type = data['type']
        tx.version = data['version']
        tx.id = data['id'] if 'id' in data else ''
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.sender_key_type = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.sender_public_key = data['senderPublicKey']
        tx.timestamp = data['timestamp']
        tx.fee = data['fee']
        tx.proofs = data['proofs']
        tx.recipient = data['recipient']
        tx.height = data['height'] if 'height' in data else ''

        if "sponsor_public_key" in data:
            tx.sponsor = data['sponsor']
            tx.sponsor_public_key = data['sponsorPublicKey']
            tx.sponsor_key_type = data['sponsorKeyType']

        return tx

