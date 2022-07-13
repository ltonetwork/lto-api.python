import base58
import struct
from lto.transaction import Transaction
from lto import crypto


class CancelLease(Transaction):
    TYPE = 9
    BASE_FEE = 100000000
    DEFAULT_VERSION = 3

    def __init__(self, lease_id: str):
        super().__init__()
        self.lease_id = lease_id
        self.tx_fee = self.BASE_FEE
        self.version = self.DEFAULT_VERSION

    def __to_binary_v2(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\02' +
                crypto.str2bytes(self.chain_id) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">Q", self.timestamp) +
                base58.b58decode(self.lease_id))

    def __to_binary_v3(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                base58.b58decode(self.lease_id))

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
            "fee": self.tx_fee,
            "timestamp": self.timestamp,
            "sponsor": self.sponsor,
            "sponsorKeyType": self.sponsor_key_type,
            "sponsorPublicKey": self.sponsor_public_key,
            "proofs": self.proofs or None,
            "leaseId": self.lease_id,
            "height": self.height
        })

    @staticmethod
    def from_data(data):
        tx = CancelLease(data['leaseId'])
        tx._init_from_data(data)

        return tx
