from abc import ABC, abstractmethod

class ciccio(ABC):
    DEFAULT_TX_FEE = 100000000

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def my_abstract_method(self):
        pass

