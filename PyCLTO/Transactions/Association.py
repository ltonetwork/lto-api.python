import base58
from PyCLTO import crypto
from time import time
from PyCLTO.Transaction import Transaction
from PyCLTO.Transactions.pack import AssociationToBinary


class Association(Transaction):
    DEFAULT_LEASE_FEE = 100000000
    TYPE = 16
    defaultVersion = 3

    def __init__(self, recipient, associationType, anchor='', expires=0):
        super().__init__()
        self.recipient = recipient
        self.associationType = associationType
        self.anchor = anchor
        self.txFee = self.DEFAULT_LEASE_FEE
        self.version = self.defaultVersion

        self.expires = expires
        current = int(time() * 1000)
        if self.expires != 0 and self.expires <= current:
            raise Exception('Wring exipration date')

    def toBinary(self):
        if self.version == 1:
            return AssociationToBinary.toBinaryV1(self)
        elif self.version == 3:
            return AssociationToBinary.toBinaryV3(self)
        else:
            raise Exception('Incorrect Version')



    def toJson(self):
        return ({
                "type": self.TYPE,
                "version": self.defaultVersion,
                "sender": self.sender,
                "senderKeyType": "ed25519",
                "senderPublicKey": self.senderPublicKey,
                "recipient": self.recipient,
                "associationType": self.associationType,
                "hash": base58.b58encode(crypto.str2bytes(self.anchor)),
                "timestamp": self.timestamp,
                "expires": self.expires,
                "fee": self.txFee,
                "proofs": self.proofs
            })

    @staticmethod
    def fromData(data):
        tx = Association(recipient='', associationType='')
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
        tx.expires = data['expires']
        tx.fee = data['fee']
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.height = data['height'] if 'height' in data else ''

        return tx

