from PyCLTO.test1 import transaction

class transfer(transaction):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount

    def printAm(self):
        print(self.amount)
        print(self.timestamp)

    def my_abstract_method(self):
        pass

newTransfer = transfer('10')
newTransfer.printAm()
print(type(transaction.amount))



