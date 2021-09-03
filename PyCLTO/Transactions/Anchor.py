import base58
from PyCLTO import crypto
from PyCLTO.Transaction import Transaction
from PyCLTO.Transactions.pack import AnchorToBinary


class Anchor(Transaction):
    TYPE = 15
    DEFAULT_ANCHOR_FEE = 35000000
    defaultVersion = 3

    def __init__(self, anchor):
        super().__init__()

        self.anchor = anchor
        self.txFee = self.DEFAULT_ANCHOR_FEE
        self.version = self.defaultVersion


    def toBinary(self):
        if self.version == 1:
            return AnchorToBinary.toBinaryV1(self)
        elif self.version == 3:
            return AnchorToBinary.toBinaryV3(self)
        else:
            raise Exception('Incorrect Version')

    def toJson(self):
        return({
            "type": self.TYPE,
            "version": self.version,
            "sender": self.sender,
            "senderKeyType": "ed25519",
            "senderPublicKey": self.senderPublicKey,
            "fee": self.txFee,
            "timestamp": self.timestamp,
            "anchors": base58.b58encode(crypto.str2bytes(self.anchor)),
            "proofs": self.proofs
            })

    @staticmethod
    def fromData(data):
        tx = Anchor(anchor='')
        tx.id = data['id'] if 'id' in data else ''
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.senderKeyType = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.senderPublicKey = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.anchors = data['anchors']
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.height = data['height'] if 'height' in data else ''
        return tx
