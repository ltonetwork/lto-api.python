import base64
import hashlib
import pyblake2
import base58

if bytes == str:  # python2
    str2bytes = lambda s: s
    bytes2str = lambda b: b
    str2list = lambda s: [ord(c) for c in s]
else:  # python3
    str2bytes = lambda s: s.encode('latin-1')
    bytes2str = lambda b: ''.join(map(chr, b))
    str2list = lambda s: [c for c in s]


def sha256(s):
    return hashlib.sha256(str2bytes(s)).digest()

def hashChain(s):
    a=pyblake2.blake2b(s, digest_size=32).digest()
    b=hashlib.sha256(a).digest()
    return ''.join(map(chr, b))

def sign(privateKey, message):
    return base58.b58encode(privateKey.sign(message).signature)

def id(message):
    return base58.b58encode(hashlib.sha256(message).digest())

def getNetwork(address):
    # Chain_ID = unpack('Cversion/anetwork', account.address)
    decodedAddress = base58.b58decode(address)
    return str(decodedAddress)[6]

def verify_signature(pub_key, message, signature):
    """ all of the arguments are expected in a string format """
    #return curve.verifySignature(base58.b58decode(pub_key), message.encode(), base58.b58decode(signature)) == 0

def decode(string: str, encoding: str):
    if encoding == 'base58':
        return base58.b58decode(string)
    elif encoding == 'base64':
        return base64.decode(string)
    elif encoding == 'hex':
        raise Exception('Hexadecimal decoding not yet implemented')
    else:
        raise Exception('Failed to decode')

def endecode(string: str, encoding: str):
    if encoding == 'base58':
        return base58.b58encode(string)
    elif encoding == 'base64':
        return base64.encode(string)
    elif encoding == 'hex':
        raise Exception('Hexadecimal encoding not yet implemented')
    else:
        raise Exception('Failed to encode')

def validateAddress(address):
    ADDRESS_VERSION = 1
    ADDRESS_CHECKSUM_LENGTH = 4
    ADDRESS_HASH_LENGTH = 20
    ADDRESS_LENGTH = 1 + 1 + ADDRESS_CHECKSUM_LENGTH + ADDRESS_HASH_LENGTH

    addr = bytes2str(base58.b58decode(address))
    if addr[0] != chr(ADDRESS_VERSION):
        raise Exception('Wrong address version')
    elif len(addr) != ADDRESS_LENGTH:
        raise Exception('Wrong address length')
    elif addr[-ADDRESS_CHECKSUM_LENGTH:] != hashChain(
            str2bytes(addr[:-ADDRESS_CHECKSUM_LENGTH]))[:ADDRESS_CHECKSUM_LENGTH]:
        raise Exception('Wrong address checksum')
    else:
        return True
