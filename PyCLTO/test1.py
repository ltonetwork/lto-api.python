from abc import ABC, abstractmethod

class transaction(ABC):
    amount = ''
    def __init__(self):
        self.timestamp = 'dall oggetto Json'



    @abstractmethod
    def my_abstract_method(self):
        pass

