import base58
import struct
from lto import crypto
from lto.binary import Binary
from lto.transaction import Transaction


class Transfer(Transaction):
    TYPE = 4
    BASE_FEE = 100000000
    DEFAULT_VERSION = 3

    def __init__(self, recipient: str, amount: int, attachment=''):
        super().__init__()
        self.recipient = recipient
        crypto.validate_address(recipient)
        self.amount = amount
        self.attachment = Binary(attachment, 'utf-8') if type(attachment) == str else Binary(attachment)
        self.version = self.DEFAULT_VERSION

        if self.amount <= 0:
            raise Exception('Amount should be positive')

        self.tx_fee = self.BASE_FEE

    def __to_binary_v2(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\2' +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.amount) +
                struct.pack(">Q", self.tx_fee) +
                base58.b58decode(self.recipient) +
                struct.pack(">H", len(self.attachment)) +
                self.attachment)

    def __to_binary_v3(self):
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
                self.attachment)

    def to_binary(self):
        if self.version == 2:
            return self.__to_binary_v2()
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
            "amount": self.amount,
            "recipient": self.recipient,
            "attachment": self.attachment.base58() if self.attachment else None,
            "sponsor": self.sponsor,
            "sponsorKeyType": self.sponsor_key_type,
            "sponsorPublicKey": self.sponsor_public_key,
            "proofs": self.proofs or None,
            "height": self.height
        })

    @staticmethod
    def from_data(data):
        tx = Transfer(data.get('recipient'), data.get('amount'), Binary.frombase58(data.get('attachment', '')))
        tx._init_from_data(data)

        return tx
