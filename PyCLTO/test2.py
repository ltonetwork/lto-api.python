'''from PyCLTO.test1 import ciccio

class bello(ciccio):
    def __init__(self, name, surname):
        super().__init__(name)
        self.surname = surname

    def test(self):
        print(ciccio.DEFAULT_TX_FEE)


    def my_abstract_method(self):
        pass



caio = bello('ciccio', 'bello')
caio.test()'''


# trying to get the network chain ID from the address

from struct import unpack, pack
import base58
from AccountFactory import AccountFactory
from nacl.signing import SigningKey
from nacl.signing import VerifyKey

account = AccountFactory("T").create()
address = '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du'

'''def getNetwork():
    Chain_ID = unpack('Cversion/anetwork', account.address)


    return Chain_ID'''


def getNetwork(address):
    # Chain_ID = unpack('Cversion/anetwork', account.address)
    decodedAddress = base58.b58decode(address)
    return str(decodedAddress)[6]
#print(getNetwork())

#print(account.publicKey)
#print(account.privateKey)
add = account.address
pubKey =account.publicKey
print(account.publicKey, " : ", type(pubKey))
print(add, " : ", type(add))

print(base58.b58encode(pubKey.__bytes__()))
decodedAdd = base58.b58decode(add)
print(decodedAdd, type(decodedAdd))
#test = '\x01T\xd1\xd6\x8d\xdfU D\xd2\xe3$\x17?85\xa3\xd9\xd7\xe1<\xd8\xd0\x03\x13';
#print(unpack("Cversion/anetwork" , decodedAdd))

print(getNetwork(account.address))




'''just need to decode it the right way, if you check at the beginning there s always T or M, need to decode it the right way,
    so look throughoutfully at the base58 encoding and decoding.'''