from PyCLTO import crypto
from PyCLTO.Transaction import Transaction
from PyCLTO.Transactions.pack import SponsorToBinary

class Sponsor(Transaction):
    TYPE = 18
    DEFAULT_SPONSOR_FEE = 500000000
    defaultVersion = 3

    def __init__(self, recipient):
        super().__init__()
        self.recipient = recipient
        crypto.validateAddress(recipient)
        self.txFee = self.DEFAULT_SPONSOR_FEE
        self.version = self.defaultVersion


    def toBinary(self):
        if self.version == 1:
            return SponsorToBinary.toBinaryV1(self)
        elif self.version == 3:
            return SponsorToBinary.toBinaryV3(self)
        else:
            raise Exception('Incorrect Version')


    def toJson(self):
        return ({
            "type": self.TYPE,
            "version": self.version,
            "senderKeyType": "ed25519",
            "sender": self.sender,
            "senderPublicKey": self.senderPublicKey,
            "recipient": self.recipient,
            "timestamp": self.timestamp,
            "fee": self.txFee,
            "proofs": self.proofs
        })

    @staticmethod
    def fromData(data):
        tx = Sponsor(data['recipient'])
        tx.type = data['type']
        tx.version = data['version']
        tx.id = data['id'] if 'id' in data else ''
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.senderKeyType = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.senderPublicKey = data['senderPublicKey']
        tx.recipient = data['recipient']
        tx.timestamp = data['timestamp']
        tx.fee = data['fee']
        tx.proofs = data['proofs']
        tx.height = data['height'] if 'height' in data else ''
        return tx

