import base58
import struct
from lto.transaction import Transaction
from lto import crypto


class CancelLease(Transaction):
    TYPE = 9
    DEFAULT_CANCEL_LEASE_FEE = 500000000
    DEFAULT_VERSION = 3


    def __init__(self, leaseId):
        super().__init__()
        self.leaseId = leaseId
        self.tx_fee = self.DEFAULT_CANCEL_LEASE_FEE
        self.version = self.DEFAULT_VERSION

    def __to_binary_V2(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\02' +
                crypto.str2bytes(self.chain_id) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">Q", self.timestamp) +
                base58.b58decode(self.leaseId))

    def __to_binary_V3(self):
        return (
                self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                base58.b58decode(self.leaseId)
                )

    def to_binary(self):
        if self.version == 2:
            return self.__to_binary_V2()
        elif self.version == 3:
            return self.__to_binary_V3()
        else:
            raise Exception('Incorrect Version')

    def to_json(self):
        return({
            "type": self.TYPE,
            "version": self.version,
            "sender": self.sender,
            "senderKeyType": self.sender_key_type,
            "senderPublicKey": self.sender_public_key,
            "fee": self.tx_fee,
            "timestamp": self.timestamp,
            "proofs": self.proofs,
            "leaseId": self.leaseId
        } | self._sponsor_json())

    @staticmethod
    def from_data(data):
        tx = CancelLease(leaseId='')
        tx.id = data['id'] if 'id' in data else ''
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.sender_key_type = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.sender_public_key = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.leaseId = data['leaseId'] if 'leaseId' in data else ''
        tx.height = data['height'] if 'height' in data else ''
        return tx



