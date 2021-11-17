from LTO import crypto
from LTO.transaction import Transaction
import struct
import base58


class Sponsorship(Transaction):
    TYPE = 18
    DEFAULT_SPONSORSHIP_FEE = 500000000
    DEFAULT_VERSION = 3

    def __init__(self, recipient):
        super().__init__()
        self.recipient = recipient
        crypto.validate_address(recipient)
        self.tx_fee = self.DEFAULT_SPONSORSHIP_FEE
        self.version = self.DEFAULT_VERSION

    def __to_binary_V1(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\1' +
                crypto.str2bytes(crypto.get_network(self.sender)) +
                base58.b58decode(self.sender_public_key) +
                base58.b58decode(self.recipient) +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.tx_fee))

    def __to_binary_V3(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                base58.b58decode(self.recipient)
                )

    def to_binary(self):
        if self.version == 1:
            return self.__to_binary_V1()
        elif self.version == 3:
            return self.__to_binary_V3()
        else:
            raise Exception('Incorrect Version')

    def to_json(self):
        return ({
                    "type": self.TYPE,
                    "version": self.version,
                    "sender": self.sender,
                    "senderKeyType": self.sender_key_type,
                    "senderPublicKey": self.sender_public_key,
                    "recipient": self.recipient,
                    "timestamp": self.timestamp,
                    "fee": self.tx_fee,
                    "proofs": self.proofs
                } | self._sponsor_json())

    @staticmethod
    def from_data(data):
        tx = Sponsorship(data['recipient'])
        tx.type = data['type']
        tx.version = data['version']
        tx.id = data['id'] if 'id' in data else ''
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.sender_key_type = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.sender_public_key = data['senderPublicKey']
        tx.recipient = data['recipient']
        tx.timestamp = data['timestamp']
        tx.fee = data['fee']
        tx.proofs = data['proofs']
        tx.height = data['height'] if 'height' in data else ''
        return tx
