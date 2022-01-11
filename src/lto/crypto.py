import base64
import hashlib
import pyblake2
import base58
import inflection
import struct

str2bytes = lambda s: s.encode('latin-1')
bytes2str = lambda b: ''.join(map(chr, b))
str2list = lambda s: [c for c in s]


def sha256(s):
    return hashlib.sha256(str2bytes(s)).digest()


def hash_chain(s):
    a = pyblake2.blake2b(s, digest_size=32).digest()
    b = hashlib.sha256(a).digest()
    return ''.join(map(chr, b))


def get_network(address):
    decoded_address = base58.b58decode(address)
    return str(decoded_address)[6]


def recode(string, from_encoding, to_encoding):
    binary = decode(string, from_encoding)
    return encode(binary, to_encoding)

def decode(string, encoding: str):
    if encoding == 'base58':
        return base58.b58decode(string)
    elif encoding == 'base64':
        return base64.b64decode(string)
    elif encoding == 'hex':
        return bytes.fromhex(string)
    else:
        raise Exception('Failed to decode')


def encode(string, encoding: str):
    if encoding == 'base58':
        return base58.b58encode(string)
    elif encoding == 'base64':
        return base64.b64encode(string)
    elif encoding == 'hex':
        return string.hex()
    else:
        raise Exception('Failed to encode')


def validate_address(address):
    ADDRESS_VERSION = 1
    ADDRESS_CHECKSUM_LENGTH = 4
    ADDRESS_HASH_LENGTH = 20
    ADDRESS_LENGTH = 1 + 1 + ADDRESS_CHECKSUM_LENGTH + ADDRESS_HASH_LENGTH

    addr = bytes2str(base58.b58decode(address))
    if addr[0] != chr(ADDRESS_VERSION):
        raise Exception('Wrong address version')
    elif len(addr) != ADDRESS_LENGTH:
        raise Exception('Wrong address length')
    elif addr[-ADDRESS_CHECKSUM_LENGTH:] != hash_chain(
            str2bytes(addr[:-ADDRESS_CHECKSUM_LENGTH]))[:ADDRESS_CHECKSUM_LENGTH]:
        raise Exception('Wrong address checksum')
    else:
        return True


def key_type_id(key_type):
    if key_type == 'ed25519':
        return b'\1'
    elif key_type == 'secp256k1':
        return b'\2'
    elif key_type == 'secp256r1':
        return b'\3'
    elif key_type == 'rsa':
        return b'\4'
    else:
        raise Exception('Key Type not supported')



def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def compare_data_transaction(data, transaction):
    for key in data:
        key2 = inflection.underscore(key)
        assert data[key] == getattr(transaction, key2)
