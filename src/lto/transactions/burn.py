import base58
import struct
from lto import crypto
from lto.transaction import Transaction


class Burn(Transaction):
    TYPE = 21
    BASE_FEE = 100000000
    DEFAULT_VERSION = 3

    def __init__(self, amount: int):
        super().__init__()
        if amount < 1:
            raise Exception("Minimum burn amount = 1")
        self.amount = amount
        self.version = self.DEFAULT_VERSION
        self.tx_fee = self.BASE_FEE

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
            "sponsor": self.sponsor,
            "sponsorKeyType": self.sponsor_key_type,
            "sponsorPublicKey": self.sponsor_public_key,
            "proofs": self.proofs or None,
            "height": self.height
        })

    @staticmethod
    def from_data(data):
        tx = Burn(data['amount'])
        tx._init_from_data(data)

        return tx
