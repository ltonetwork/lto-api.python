from abc import ABC, abstractmethod
import base58

class Transaction(ABC):

    DEFAULT_TX_FEE = 100000000
    DEFAULT_SPONSOR_FEE = 500000000
    DEFAULT_SCRIPT_FEE = 500000000

    def __init__(self):
        pass

    def getNetwork(address):
        # Chain_ID = unpack('Cversion/anetwork', account.address)
        decodedAddress = base58.b58decode(address)
        return str(decodedAddress)[6]

    '''@abstractmethod
    def my_abstract_method(self):
        pass'''
