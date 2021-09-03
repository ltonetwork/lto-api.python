import base58
from PyCLTO import crypto
from PyCLTO.Transaction import Transaction
from PyCLTO.Transactions.pack import RevokeAssociationToBinary


class RevokeAssociation(Transaction):
    TYPE = 17
    DEFAULT_LEASE_FEE = 100000000
    defaultVersion = 3

    def __init__(self, recipient, associationType, anchor = ''):
        super().__init__()
        self.recipient = recipient
        self.anchor = anchor
        self.associationType = associationType

        self.txFee = self.DEFAULT_LEASE_FEE
        self.version = self.defaultVersion


    def toBinary(self):
        if self.version == 1:
            return RevokeAssociationToBinary.toBinaryV1(self)
        elif self.version == 3:
            return RevokeAssociationToBinary.toBinaryV3(self)
        else:
            raise Exception('Incorrect Version')

    def toJson(self):
        return ({
            "type": self.TYPE,
            "version": self.version,
            "sender": self.senderPublicKey,
            "senderKeyType": "ed25519",
            "senderPublicKey": self.senderPublicKey,
            "recipient": self.recipient,
            "associationType": self.associationType,
            "hash": base58.b58encode(crypto.str2bytes(self.anchor)),
            "timestamp": self.timestamp,
            "fee": self.txFee,
            "proofs": self.proofs
        })

    @staticmethod
    def fromData(data):
        tx = RevokeAssociation(recipient='', associationType='')
        tx.type = data['type']
        tx.version = data['version']
        tx.id = data['id'] if 'id' in data else ''
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.senderKeyType = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.senderPublicKey = data['senderPublicKey']
        tx.recipient = data['recipient']
        tx.associationType = data['associationType']
        tx.hash = data['hash']
        tx.timestamp = data['timestamp']
        tx.fee = data['fee']
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.height = data['height'] if 'height' in data else ''
        return tx