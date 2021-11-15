import base58
import struct
from LTO import crypto
from LTO.transaction import Transaction


class Transfer(Transaction):
    TYPE = 4
    DEFAULT_TX_FEE = 100000000
    DEFAULT_VERSION = 3

    def __init__(self, recipient, amount, attachment=''):
        super().__init__()
        self.recipient = recipient
        crypto.validate_address(recipient)
        self.amount = amount
        self.attachment = attachment
        self.version = self.DEFAULT_VERSION

        if self.amount <= 0:
            raise Exception('Amount should be positive')

        self.tx_fee = self.DEFAULT_TX_FEE

    def __to_binary_V2(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\2' +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.amount) +
                struct.pack(">Q", self.tx_fee) +
                base58.b58decode(self.recipient) +
                struct.pack(">H", len(self.attachment)) +
                crypto.str2bytes(self.attachment))

    def __to_binary_V3(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                base58.b58decode(self.recipient) +
                struct.pack(">Q", self.amount) +
                struct.pack(">H", len(self.attachment)) +
                crypto.str2bytes(self.attachment))

    def to_binary(self):
        if self.version == 2:
            return self.__to_binary_V2()
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
                    "fee": self.tx_fee,
                    "timestamp": self.timestamp,
                    "amount": self.amount,
                    "recipient": self.recipient,
                    "attachment": base58.b58encode(crypto.str2bytes(self.attachment)),
                    "proofs": self.proofs
                } | self._sponsor_json())

    @staticmethod
    def from_data(data):
        tx = Transfer(data['recipient'], data['amount'])
        tx.id = data['id'] if 'id' in data else ''
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.sender_key_type = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.sender_public_key = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.amount = data['amount']
        tx.recipient = data['recipient']
        tx.attachment = data['attachment'] if 'attachment' in data else ''
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.height = data['height'] if 'height' in data else ''

        if 'sponsorPublicKey' in data:
            tx.sponsor = data['sponsor']
            tx.sponsor_public_key = data['sponsorPublicKey']

        return tx
