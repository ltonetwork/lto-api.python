import base58
from lto import crypto
from lto.transaction import Transaction
import struct


class Register(Transaction):
    TYPE = 20
    DEFAULT_FEE = 35000000
    DEFAULT_VERSION = 3

    def __init__(self, **accounts):
        super().__init__()

        self.accounts = accounts
        self.tx_fee = self.DEFAULT_FEE
        self.version = self.DEFAULT_VERSION

        if len(self.accounts) > 100:
            raise Exception('Too many accounts')

    def __accounts_data(self):
        data = b''
        
        for i in range(0, len(self.accounts)):
            data += crypto.key_type_id(self.accounts.key_type)
            data += base58.b58decode(self.accounts.public_key)
        
        return data
    
    def __to_binary_V3(self):
        return (
                self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">H", self.keys.length) +
                self.__accounts_data()
        )

    def to_binary(self):
        if self.version == 3:
            return self.__to_binary_V3()
        else:
            raise Exception('Incorrect Version')

    def to_json(self):
        return (crypto.merge_dicts(
            {
                "type": self.TYPE,
                "version": self.version,
                "sender": self.sender,
                "senderKeyType": self.sender_key_type,
                "senderPublicKey": self.sender_public_key,
                "fee": self.tx_fee,
                "timestamp": self.timestamp,
                "accounts": map(lambda account: account.to_json(), self.accounts),
                "proofs": self.proofs
            },
            self._sponsor_json()))

    @staticmethod
    def from_data(data):
        tx = Anchor(anchor='')
        tx.id = data['id'] if 'id' in data else ''
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.sender_key_type = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.sender_public_key = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.anchors = data['anchors']
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.height = data['height'] if 'height' in data else ''
        return tx