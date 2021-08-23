import base64
import os
from datetime import time

import nacl.bindings
from nacl.signing import SigningKey, VerifyKey

import PyCLTO.crypto as crypto
import struct
import json
import base58
import logging
from PyCLTO import PublicNode


class Account(object):

    def __init__(self, address, publicKey:VerifyKey, privateKey:SigningKey = '', seed='', nonce=0):
        self.address = address
        self.publicKey = publicKey
        self.privateKey = privateKey
        self.seed = seed
        self.nonce = nonce

    def sign(self, message):
        if (self.privateKey == ''):
            raise Exception("Private key not set")
        return base58.b58encode(self.privateKey.sign(message).signature)

    def getPublicKey(self):
        return base58.b58encode(bytes(self.publicKey))


