from PyCLTO.test1 import ciccio

class bello(ciccio):
    def __init__(self, name, surname):
        super().__init__(name)
        self.surname = surname

    def test(self):
        print(ciccio.DEFAULT_TX_FEE)


    def my_abstract_method(self):
        pass



caio = bello('ciccio', 'bello')
caio.test()