from abc import ABC, abstractmethod


class Transaction(ABC):

    def __init__(self):
        self.name = 'giovanni'

    @abstractmethod
    def toBinary(self):
        pass

    def sum(self, a, b):
        return a + b



