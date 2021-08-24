import json

from PyCLTO import AccountFactory
from PyCLTO.Transactions import Anchor
from PyCLTO.Transactions import Transfer
from PyCLTO import PublicNode
from PyCLTO import crypto
import hashlib

import base58

factory = AccountFactory("T")


def Transact(amount):
    sender = factory.createFromSeed(
        "cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy")
    recipient = factory.createFromSeed(
        "north sibling rural deal find august paddle violin glow crucial inject goat habit toddler biology")

    transfer = Transfer.Transfer(recipient.address, amount*100000000)
    transfer.signWith(sender)


    url = 'https://testnet.lto.network'
    node = PublicNode(url)

    #node.broadcast(transfer)

#Transact(5)

def Anch():
    sender = factory.createFromSeed(
        "cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy")


    anchor = 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f'
    anchorTransaction = Anchor.anchor(anchor)
    anchorTransaction.signWith(sender)

    url = 'https://testnet.lto.network'
    node = PublicNode(url)
    resp = node.broadcast(anchorTransaction)
    print(resp)
    print(json.dumps(anchorTransaction.toJson()))


#Anch()


#print(type(acc.publicKey))
#print(type(acc.privateKey))
'''print(base58.b58encode(acc.publicKey.__bytes__()))
print(acc.address)

acc.publicKey.verify(signed)'''


'''def verifySignature(self, signature: str, message: str, encoding: str = 'base58'):
    if not self.publicKey:
        raise Exception('Unable to verify message; no public sign key')

    rawSignature = crypto.decode(signature, encoding)

    return len(rawSignature) == self.SODIUM_CRYPTO_SIGN_BYTES \
           and len(self.publicKey) == self.SODIUM_CRYPTO_SIGN_PUBLICKEYBYTES



  return self.publicKey.verify(signature, sData)'''


from nacl.signing import VerifyKey, SigningKey


private_key = SigningKey.generate()
message = b"Attack at Dawn"
signature = private_key.sign(message).signature
signed_messag = private_key.sign(message)
public_key = private_key.verify_key

print(type(public_key))                                                    # <class 'nacl.signing.VerifyKey'>
print(public_key.verify(signed_messag.message, signed_messag.signature))   # b'Attack at Dawn'
print(public_key.verify(signed_messag))                                    # b'Attack at Dawn'
print("signature", signature)                                                           # b'\x08\x8cl\x00\xa7;(t \xaf\x80\xbf\xe2&\xad\xc5j\x
print(signed_messag.signature)                                             # b'\x08\x8cl\x00\xa7;(t \xaf\x80\xbf\xe2&\xad\xc5j\x
print(signed_messag)                                                       # signature + message
print(type(signed_messag))                                                 # <class 'nacl.signing.SignedMessage'>
print(type(signed_messag.message))


acc = factory.createFromSeed('df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8')
recipient = factory.createFromSeed("north sibling rural deal find august paddle violin glow crucial inject goat habit toddler biology")

transaction = Transfer.Transfer(recipient.address, 1*100000000)
transaction.signWith(acc)
sign = (base58.b58decode(transaction.signature))
print("sign = ", transaction.signature)
print("sign decoded = ", sign)
sign = sign[:-1] + bytes([int(sign[-1]) ^ 1])
print(acc.publicKey.verify(transaction.toBinary(), base58.b58decode(transaction.signature)))
print('hello')
print(acc.verifySignature(transaction.toBinary(), transaction.signature))


#base58.b58encode(crypto.str2bytes(attachment))
print(base58.b58encode(crypto.str2bytes('Hello')))
print(crypto.bytes2str(base58.b58decode('9Ajdvzr')))

transaction = Transfer.Transfer('3N9ChkxWXqgdWLLErWFrSwjqARB6NtYsvZh', 120000000, 'Hello')
print(transaction.toJson())