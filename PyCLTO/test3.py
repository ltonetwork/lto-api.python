import json

from PyCLTO import AccountFactory
from PyCLTO.Transactions import Anchor
from PyCLTO.Transactions import Transfer
from PyCLTO import PublicNode
from PyCLTO import crypto
import hashlib

import base58

def testTransaction(amount):
    factory = AccountFactory("T")
    sender = factory.createFromSeed(
        "cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy")
    recipient = factory.createFromSeed(
        "north sibling rural deal find august paddle violin glow crucial inject goat habit toddler biology")

    transfer = Transfer.Transfer(recipient.address, amount*100000000)
    transfer.signWith(sender)
    #hash = '66e86a1a02d3bd884f7000d67d6a8dfa624b3b65c00fc26a981030357d2ea489'
    #trans = Anchor.Anchor(hash)
    #trans.signWith(sender)

    url = 'https://testnet.lto.network'
    node = PublicNode(url)

    node.broadcast(transfer)

#testTransaction(5)

def testAnchor():
    factory = AccountFactory("T")
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


#testAnchor()

