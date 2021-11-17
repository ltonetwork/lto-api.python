import base64
from lto.transaction import Transaction
import struct
from lto import crypto
import base58
from lto.public_node import PublicNode

class SetScript(Transaction):
    TYPE = 13
    DEFAULT_SCRIPT_FEE = 500000000
    DEFAULT_VERSION = 3

    def __init__(self, script):
        super().__init__()

        self.script = script
        if script:
            self.compiled_script = PublicNode('https://nodes.lto.network').compile(script)
        else:
            self.compiled_script = ""

        self.tx_fee = self.DEFAULT_SCRIPT_FEE
        self.version = self.DEFAULT_VERSION

    def __to_binary_V1(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\1' +
                crypto.str2bytes(crypto.get_network(self.sender)) +
                base58.b58decode(self.sender_public_key) +
                b'\1' +
                struct.pack(">H", len(self.compiled_script)) +
                self.compiled_script +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">Q", self.timestamp))

    def __to_binary_V3(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">H", len(base64.b64decode(self.compiled_script[7:]))) +
                base64.b64decode(self.compiled_script[7:])
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
            "script": str(self.compiled_script),
            "timestamp": self.timestamp,
            "fee": self.tx_fee,
            "proofs": self.proofs
        } | self._sponsor_json())

    @staticmethod
    def from_data(data):
        tx = SetScript(data['script'])
        tx.id = data['id'] if 'id' in data else ''
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.sender_key_type = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.sender_public_key = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.proofs = data['proofs']
        tx.script = data['script']
        tx.height = data['height'] if 'height' in data else ''
        return tx
