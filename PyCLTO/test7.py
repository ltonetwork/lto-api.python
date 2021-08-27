import time

class Dog():

    def __init__(self, name):
        self.name = name

    def makeNoise(self):
        print("Wooof")
        time.sleep(2)
        return ('Wooof')