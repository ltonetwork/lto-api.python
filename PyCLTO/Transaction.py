from abc import ABC, abstractmethod
from PyCLTO.Account import Account
from time import time
from PyCLTO import PublicNode
from PyCLTO.Transactions.Transfer import Transfer


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

    def signWith(self, account: Account):
        if self.timestamp == 0:
            self.timestamp = int(time() * 1000)

        if self.sender == '':
            self.sender = account.address
            self.senderPublicKey = account.getPublicKey()

        binary = self.toBinary()
        self.proofs.append(account.sign(binary))

    def broadcastTo(self, node: PublicNode):
        return node.broadcast(self)

    def fromData(self, data):

        if data['type'] == 4:
            return Transfer.fromData(data)
        elif data['type'] == 1:
            return 2
        else:
            raise Exception('No TYPE found')
