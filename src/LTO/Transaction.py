from abc import ABC, abstractmethod
from time import time
from LTO.PublicNode import PublicNode
from LTO.Account import Account



class Transaction(ABC):

    def __init__(self):

        self.txFee = 0
        self.timestamp = 0

        self.proofs = []
        self.sender = ''
        self.senderPublicKey = ''
        self.chainId = ''

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

        self.chainId = account.getNetwork()

        binary = self.toBinary()
        self.proofs.append(account.sign(binary))

    def broadcastTo(self, node: PublicNode):
        return node.broadcast(self)

    def __getattr__(self, item):
        return getattr(self, item)
