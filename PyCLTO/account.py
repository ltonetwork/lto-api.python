import base64
import os
from datetime import time

import nacl.bindings

import PyCLTO.crypto as crypto
import struct
import json
import base58
import logging
from PyCLTO import PublicNode


class pyAccount(object):

    def __init__(self, address, publicKey, privateKey='', seed='', nonce=0):
        self.address = address
        self.publicKey = publicKey
        self.privateKey = privateKey
        self.seed = seed
        self.nonce = nonce

    def sign(self, message):
        return base58.b58encode(self.privateKey.sign(message).signature)
