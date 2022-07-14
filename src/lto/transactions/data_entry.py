from lto import crypto
import struct


class DataEntry:
    def __init__(self, key: str, type: str, value):
        self.key = key
        self.type = type
        self.value = value

    def to_binary(self):
        key_bytes = crypto.str2bytes(self.key)
        return struct.pack(">H", len(key_bytes)) + key_bytes + self.__value_to_binary()

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


def dict_to_data(dictionary):
    data = []
    for key in dictionary:
        data.append(DataEntry.guess(key, dictionary[key]))
    return data


def data_to_dict(data):
    dictionary = {}
    for entry in data:
        dictionary[entry.key] = entry.value
    return dictionary
