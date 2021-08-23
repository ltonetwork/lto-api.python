from abc import ABC, abstractmethod
import base58
from PyCLTO.Account import Account
from time import time

class Transaction(ABC):

    def __init__(self):

        self.txFee = 0
        self.timestamp = 0

        self.signature = ''
        self.sender = ''
        self.senderPublicKey = ''

    @abstractmethod
    def toBinary(self):
        pass

    def signWith(self, account: Account):
        if self.timestamp == 0:
            self.timestamp = int(time() * 1000)

        self.sender = account.address
        self.senderPublicKey = account.getPublicKey()

        sData = self.toBinary()
        self.signature = account.sign(sData)




    '''@abstractmethod
    def my_abstract_method(self):
        pass'''
