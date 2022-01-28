import base58
from lto import crypto
import struct

from lto.transaction import Transaction


class MassTransfer(Transaction):
    BASE_FEE = 100000000
    VAR_FEE = 10000000
    TYPE = 11
    DEFAULT_VERSION = 3

    def __init__(self, transfers, attachment=''):
        super().__init__()
        self.transfers = transfers
        self.attachment = attachment
        self.transfers_data = ''
        self.tx_fee = self.BASE_FEE + (len(self.transfers) * self.VAR_FEE)
        self.version = self.DEFAULT_VERSION

        if len(self.transfers) > 100:
            raise Exception('Too many recipients')

    def __transfers_to_binary(self):
        data = b''
        for transfer in self.transfers:
            data += base58.b58decode(transfer['recipient'])
            data += struct.pack(">Q", transfer['amount'])

        return data

    def __to_binary_v1(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\1' +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">H", len(self.transfers)) +
                self.__transfers_to_binary() +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">H", len(self.attachment)) +
                crypto.str2bytes(self.attachment))

    def __to_binary_v3(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">H", len(self.transfers)) +
                self.__transfers_to_binary() +
                struct.pack(">H", len(self.attachment)) +
                crypto.str2bytes(self.attachment))

    def to_binary(self):
        if self.version == 1:
            return self.__to_binary_v1()
        elif self.version == 3:
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
            "proofs": self.proofs,
            "attachment": base58.b58encode(crypto.str2bytes(self.attachment)),
            "transfers": self.transfers,
            "height": self.height if self.height else ""
        }, self._sponsor_json()))

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

        if "sponsor_public_key" in data:
            tx.sponsor = data['sponsor']
            tx.sponsor_public_key = data['sponsorPublicKey']
            tx.sponsor_key_type = data['sponsorKeyType']

        return tx

