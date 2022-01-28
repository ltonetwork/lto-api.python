import base58
from lto import crypto
from lto.transaction import Transaction
import struct
import math


class Data(Transaction):
    TYPE = 12
    BASE_FEE = 100000000
    VAR_FEE = 10000000
    VAR_BYTES = 256
    DEFAULT_VERSION = 3

    def __init__(self, data):
        super().__init__()

        self.data = self.__dict_to_data(data) if type(data) == dict else data
        self.tx_fee = self.BASE_FEE + math.ceil((len(self.__data_to_binary()) / self.VAR_BYTES)) * self.VAR_FEE
        self.version = self.DEFAULT_VERSION

    @staticmethod
    def __dict_to_data(dictionary):
        data = []
        for key in dictionary:
            data.append(DataEntry.guess(key, dictionary[key]))
        return data

    def __data_to_binary(self):
        binary = b''
        for entry in self.data:
            binary += entry.to_binary()
        return binary

    def __to_binary_v3(self):
        data_binary = self.__data_to_binary()

        return (self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">H", len(self.data)) +
                data_binary)

    def to_binary(self):
        if self.version == 3:
            return self.__to_binary_v3()
        else:
            raise Exception('Incorrect Version')

    def to_json(self):
        return (crypto.merge_dicts({
                "id": self.id if self.id else "",
                "type": self.TYPE,
                "version": self.version,
                "sender": self.sender,
                "senderKeyType": self.sender_key_type,
                "senderPublicKey": self.sender_public_key,
                "fee": self.tx_fee,
                "timestamp": self.timestamp,
                "data": list(map(lambda entry: entry.to_json(), self.data)),
                "proofs": self.proofs,
                "height": self.height if self.height else ""
            },
            self._sponsor_json()))

    def data_as_dict(self):
        dictionary = {}
        for entry in self.data:
            dictionary[entry.key] = entry.value
        return dictionary

    @staticmethod
    def from_data(data):
        tx = Data([])
        tx.id = data['id'] if 'id' in data else ''
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.sender_key_type = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.sender_public_key = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.data = list(map(DataEntry.from_data, data['data'])) if 'data' in data else ''
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.height = data['height'] if 'height' in data else ''
        return tx


class DataEntry:
    def __init__(self, key, type, value):
        self.key = key
        self.type = type
        self.value = value

    def to_binary(self):
        key_bytes = crypto.str2bytes(self.key)
        return (
                struct.pack(">H", len(key_bytes)) +
                key_bytes +
                self.__value_to_binary()
        )

    def __value_to_binary(self):
        if self.type == 'integer':
            return b'\0' + struct.pack(">Q", self.value)
        elif self.type == 'boolean':
            return b'\1' + (b'\1' if self.value else b'\0')
        elif self.type == 'binary':
            byte_val = crypto.str2bytes(self.value)
            return b'\2' + struct.pack(">H", len(byte_val)) + byte_val
        elif self.type == 'string':
            byte_val = crypto.str2bytes(self.value)
            return b'\3' + struct.pack(">H", len(byte_val)) + byte_val
        else:
            raise Exception('Data Type not supported')

    @staticmethod
    def from_data(data):
        return DataEntry(data['key'], data['type'], data['value'])

    @staticmethod
    def guess(key, value):
        if type(value) == int:
            return DataEntry(key, 'integer', value)
        elif type(value) == bool:
            return DataEntry(key, 'boolean', value)
        elif type(value) == bytes:
            return DataEntry(key, 'binary', value)
        elif type(value) == str:
            return DataEntry(key, 'string', value)
        else:
            raise Exception('Unable to determine type of data entry')

    def to_json(self):
        return {
            "key": self.key,
            "type": self.type,
            "value": self.value
        }
