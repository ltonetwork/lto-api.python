from PyCLTO.test2 import Transaction

class Transfer(Transaction):

    def __init__(self, recipient, amount):
        super().__init__()
        self.recipient = recipient
        self.amount = amount

    def toBinary(self):
        return self.amount+150

    def mul(self, a, b):
        return a * b

    @staticmethod
    def fromData(data, **kwargs):
        return data - 2



