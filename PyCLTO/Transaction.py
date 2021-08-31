import json
from abc import ABC, abstractmethod
import PyCLTO.Account
from time import time
import PyCLTO.PublicNode
import PyCLTO

class Transaction(ABC):

    def __init__(self):

        self.txFee = 0
        self.timestamp = 0

        self.proofs = []
        self.sender = ''
        self.senderPublicKey = ''

    @abstractmethod
    def toBinary(self):
        pass

    def isSigned(self):
        return len(self.proofs) != 0

    def signWith(self, account: PyCLTO.Account):
        if self.timestamp == 0:
            self.timestamp = int(time() * 1000)

        if self.sender == '':
            self.sender = account.address
            self.senderPublicKey = account.getPublicKey()

        binary = self.toBinary()
        self.proofs.append(account.sign(binary))

    def broadcastTo(self, node: PyCLTO.PublicNode):
        return node.broadcast(self)

    def fromData(self, data):

        if type(data) != dict:
            data = json.loads(data)

        if data['type'] == 4:
            return PyCLTO.Transactions.Transfer.Transfer.fromData(data)
        elif data['type'] == 1:
            return 2
        else:
            raise Exception('No TYPE found')
