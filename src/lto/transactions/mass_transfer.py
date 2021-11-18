import base58
from lto import crypto
import struct

from lto.transaction import Transaction


class MassTransfer(Transaction):
    DEFAULT_BASE_FEE = 100000000
    TYPE = 11
    DEFAULT_VERSION = 3

    def __init__(self, transfers, attachment=''):
        super().__init__()
        self.transfers = transfers
        self.attachment = attachment
        self.transfers_data = ''
        self.base_fee = self.DEFAULT_BASE_FEE
        self.tx_fee = self.base_fee + int(len(self.transfers) * self.base_fee / 10)
        self.version = self.DEFAULT_VERSION

        if len(self.transfers) > 100:
            raise Exception('Too many recipients')

        self.transfers_data = b''
        for i in range(0, len(self.transfers)):
            self.transfers_data += base58.b58decode(self.transfers[i]['recipient']) \
                             + struct.pack(">Q", self.transfers[i]['amount'])

    def __to_binary_V1(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\1' +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">H", len(self.transfers)) +
                self.transfers_data +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">H", len(self.attachment)) +
                crypto.str2bytes(self.attachment))

    def __to_binary_V3(self):
        return (
                self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">H", len(self.transfers)) +

                self.transfers_data +

                struct.pack(">H", len(self.attachment)) +
                crypto.str2bytes(self.attachment))

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
            "fee": self.tx_fee,
            "timestamp": self.timestamp,
            "proofs": self.proofs,
            "attachment": base58.b58encode(crypto.str2bytes(self.attachment)),
            "transfers": self.transfers
        } | self._sponsor_json())

    @staticmethod
    def from_data(data):
        tx = MassTransfer(transfers='')
        tx.type = data['type']
        tx.version = data['version']
        tx.id = data['id'] if 'id' in data else ''
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.sender_key_type = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.sender_public_key = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.attachment = data['attachment'] if 'attachment' in data else ''
        tx.transfers = data['transfers']
        tx.height = data['height'] if 'height' in data else ''
        return tx

