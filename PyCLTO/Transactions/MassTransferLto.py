import base58
from PyCLTO import crypto
import struct
from PyCLTO.Transaction import Transaction
from PyCLTO.Transactions.pack import MassTransferToBinary


class MassTransferLTO(Transaction):
    DEFAULT_BASE_FEE = 100000000
    TYPE = 11
    defaultVersion = 3

    def __init__(self, transfers, attachment=''):
        super().__init__()
        self.transfers = transfers
        self.attachment = attachment
        self.transfersData = ''
        self.baseFee = self.DEFAULT_BASE_FEE
        self.txFee = self.baseFee + int(len(self.transfers) * self.baseFee / 10)
        self.version = self.defaultVersion

        if len(self.transfers) > 100:
            raise Exception('Too many recipients')

        self.transfersData = b''
        for i in range(0, len(self.transfers)):
            self.transfersData += base58.b58decode(self.transfers[i]['recipient']) \
                             + struct.pack(">Q", self.transfers[i]['amount'])


    def toBinary(self):
        if self.version == 1:
            return MassTransferToBinary.toBinaryV1(self)
        elif self.version == 3:
            return MassTransferToBinary.toBinaryV3(self)
        else:
            raise Exception('Incorrect Version')


    def toJson(self):
        return ({
            "type": self.TYPE,
            "version": self.version,
            "sender": self.sender,
            "senderKeyType": "ed25519",
            "senderPublicKey": self.senderPublicKey,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "proofs": self.proofs,
            "attachment": base58.b58encode(crypto.str2bytes(self.attachment)),
            "transfers": self.transfers
        })

    @staticmethod
    def fromData(data):
        tx = MassTransferLTO(transfers='')
        tx.type = data['type']
        tx.version = data['version']
        tx.id = data['id'] if 'id' in data else ''
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.senderKeyType = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.senderPublicKey = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.attachment = data['attachment'] if 'attachment' in data else ''
        tx.transfers = data['transfers']
        tx.height = data['height'] if 'height' in data else ''
        return tx

