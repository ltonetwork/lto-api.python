class Dog(object):
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def abbaia(self):
        print(self.sound + ' !!')

cane = Dog('Ciccio', "Woooooof")
cane.abbaia()