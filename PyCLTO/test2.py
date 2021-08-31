from abc import ABC, abstractmethod
import PyCLTO

class fii(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def whatever(self):
        pass

    def sum(self, a, b):
        return a + b

print(PyCLTO.test3.foo('name').mul(1,3))