import base58
from lto import crypto
import struct

from lto.binary import Binary
from lto.transaction import Transaction


class MassTransfer(Transaction):
    BASE_FEE = 100000000
    VAR_FEE = 10000000
    TYPE = 11
    DEFAULT_VERSION = 3

    def __init__(self, transfers: list, attachment=''):
        super().__init__()
        self.transfers = transfers
        self.attachment = Binary(attachment, 'utf-8') if type(attachment) == str else Binary(attachment)
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
                self.attachment)

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
                self.attachment)

    def to_binary(self):
        if self.version == 1:
            return self.__to_binary_v1()
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
            "attachment": self.attachment.base58() if self.attachment else None,
            "transfers": self.transfers,
            "sponsor": self.sponsor,
            "sponsorKeyType": self.sponsor_key_type,
            "sponsorPublicKey": self.sponsor_public_key,
            "proofs": self.proofs or None,
            "height": self.height
        })

    @staticmethod
    def from_data(data):
        tx = MassTransfer(data['transfers'], Binary.frombase58(data.get('attachment', '')))
        tx._init_from_data(data)

        return tx
