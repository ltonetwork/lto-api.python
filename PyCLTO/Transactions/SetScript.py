import base64
from PyCLTO.Transaction import Transaction
from PyCLTO.Transactions.pack import SetScriptToBinary


class SetScript(Transaction):
    TYPE = 13
    DEFAULT_SCRIPT_FEE = 500000000
    defaultVersion = 3

    def __init__(self, script):
        super().__init__()

        self.script = script
        self.compiledScript = base64.b64decode(self.script)

        self.txFee = self.DEFAULT_SCRIPT_FEE
        self.version = self.defaultVersion


    def toBinary(self):
        if self.version == 1:
            return SetScriptToBinary.toBinaryV1(self)
        elif self.version == 3:
            return SetScriptToBinary.toBinaryV3(self)
        else:
            raise Exception('Incorrect Version')

    def toJson(self):
        return ({
            "type": self.TYPE,
            "version": self.defaultVersion,
            "sender": self.sender,
            "senderKeyType": "ed25519",
            "senderPublicKey": self.senderPublicKey,
            "script": 'base64:' + str(self.script),
            "timestamp": self.timestamp,
            "fee": self.txFee,
            "proofs": self.proofs
        })

    @staticmethod
    def fromData(data):
        tx = SetScript(data['script'])
        tx.id = data['id'] if 'id' in data else ''
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.senderKeyType = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.senderPublicKey = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.proofs = data['proofs']
        tx.script = data['script']
        tx.height = data['height'] if 'height' in data else ''
        return tx