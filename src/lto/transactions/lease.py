import base58
from lto import crypto
import struct
from lto.transaction import Transaction


class Lease(Transaction):
    BASE_FEE = 100000000
    TYPE = 8
    DEFAULT_VERSION = 3

    def __init__(self, recipient: str, amount: int):
        super().__init__()
        self.amount = amount
        self.recipient = recipient
        self.tx_fee = self.BASE_FEE
        self.version = self.DEFAULT_VERSION
        if self.amount <= 0:
            raise Exception('Amount must be > 0')

    def __to_binary_v2(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\2' +
                b'\0' +
                base58.b58decode(self.sender_public_key) +
                base58.b58decode(self.recipient) +
                struct.pack(">Q", self.amount) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">Q", self.timestamp))

    def __to_binary_v3(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                base58.b58decode(self.recipient) +
                struct.pack(">Q", self.amount))

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
            "recipient": self.recipient,
            "amount": self.amount,
            "fee": self.tx_fee,
            "timestamp": self.timestamp,
            "sponsor": self.sponsor,
            "sponsorKeyType": self.sponsor_key_type,
            "sponsorPublicKey": self.sponsor_public_key,
            "proofs": self.proofs or None,
            "height": self.height
        })

    @staticmethod
    def from_data(data):
        tx = Lease(data['recipient'], data['amount'])
        tx._init_from_data(data)

        return tx
