import base58
import struct
from lto.transaction import Transaction
from lto import crypto


class CancelLease(Transaction):
    TYPE = 9
    DEFAULT_FEE = 100000000
    DEFAULT_VERSION = 3


    def __init__(self, lease_id):
        super().__init__()
        self.lease_id = lease_id
        self.tx_fee = self.DEFAULT_FEE
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
        return(crypto.merge_dicts({
            "id": self.id if self.id else "",
            "type": self.TYPE,
            "version": self.version,
            "sender": self.sender,
            "senderKeyType": self.sender_key_type,
            "senderPublicKey": self.sender_public_key,
            "fee": self.tx_fee,
            "timestamp": self.timestamp,
            "proofs": self.proofs,
            "leaseId": self.lease_id,
            "height": self.height if self.height else ""
        },
        self._sponsor_json()))

    @staticmethod
    def from_data(data):
        tx = CancelLease(lease_id='')
        tx.id = data['id'] if 'id' in data else ''
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.sender_key_type = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.sender_public_key = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.lease_id = data['leaseId'] if 'leaseId' in data else ''
        tx.height = data['height'] if 'height' in data else ''

        if "sponsor_public_key" in data:
            tx.sponsor = data['sponsor']
            tx.sponsor_public_key = data['sponsorPublicKey']
            tx.sponsor_key_type = data['sponsorKeyType']

        return tx



