import PyCLTO

class foo(PyCLTO.test2.fii):

    def __init__(self, name):
        super().__init__(name)
        print('this is foo')

    def whatever(self):
        print('hello')

    def mul(self, a, b):
        return a * b

'''foo('ciccio')
print(foo('gino').name)'''


