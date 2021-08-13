from abc import ABC, abstractmethod

class Transaction(ABC):

    DEFAULT_TX_FEE = 100000000
    DEFAULT_SPONSOR_FEE = 500000000

    def __init__(self):
        pass

    '''@abstractmethod
    def my_abstract_method(self):
        pass'''
