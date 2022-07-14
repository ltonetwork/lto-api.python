import base58
import struct
import math
from lto import crypto
from lto.transaction import Transaction
from lto.transactions.data_entry import DataEntry, dict_to_data, data_to_dict


class Data(Transaction):
    TYPE = 12
    BASE_FEE = 50000000
    VAR_FEE = 10000000
    VAR_BYTES = 256
    DEFAULT_VERSION = 3

    def __init__(self, data):
        super().__init__()

        self.version = self.DEFAULT_VERSION
        self.data = dict_to_data(data) if type(data) == dict else data
        self.tx_fee = self.BASE_FEE + math.ceil((len(self.__data_to_binary()) / self.VAR_BYTES)) * self.VAR_FEE

    def __data_to_binary(self):
        binary = b''
        for entry in self.data:
            binary += entry.to_binary()
        return binary

    def __to_binary_v3(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">H", len(self.data)) +
                self.__data_to_binary())

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
                "data": [entry.to_json() for entry in self.data],
                "sponsor": self.sponsor,
                "sponsorKeyType": self.sponsor_key_type,
                "sponsorPublicKey": self.sponsor_public_key,
                "proofs": self.proofs or None,
                "height": self.height
            })

    def data_as_dict(self):
        return data_to_dict(self.data)

    @staticmethod
    def from_data(data):
        tx = Data([DataEntry.from_data(entry) for entry in data.get('data', [])])
        tx._init_from_data(data)

        return tx

