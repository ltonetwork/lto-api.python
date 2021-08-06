# Copyright (C) 2017 PyWaves Developers
#
# This file is part of PyWaves.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

from __future__ import absolute_import, division, print_function, unicode_literals

import requests

from .PublicNode import PublicNode
from .account import *
from .coin import *


class PyCLTO:
    def __init__(self, chainId = 'T'):

        from PyCLTO.AccountFactory import AccountFactory
        self.accountFactory = AccountFactory(chainId)
        self.publicNode = PublicNode('https://testnet.lto.network')

        self.DEFAULT_TX_FEE = 100000000
        self.DEFAULT_BASE_FEE = self.DEFAULT_TX_FEE
        self.DEFAULT_SMART_FEE = 400000
        self.DEFAULT_LEASE_FEE = 100000000
        self.DEFAULT_SPONSOR_FEE = 500000000
        self.DEFAULT_SCRIPT_FEE = 500000000
        self.DEFAULT_CURRENCY = 'LTO'
        self.VALID_TIMEFRAMES = (5, 15, 30, 60, 240, 1440)
        self.MAX_WDF_REQUEST = 100

        self.THROW_EXCEPTION_ON_ERROR = False

        self.OFFLINE = False
        self.NODE = 'https://testnet.lto.network'
        #self.NODE = 'https://nodes.lto.network'

        self.ADDRESS_VERSION = 1
        self.ADDRESS_CHECKSUM_LENGTH = 4
        self.ADDRESS_HASH_LENGTH = 20
        self.ADDRESS_LENGTH = 1 + 1 + self.ADDRESS_CHECKSUM_LENGTH + self.ADDRESS_HASH_LENGTH

        #self.CHAIN = 'mainnet'
        self.CHAIN = 'testnet'
        #self.CHAIN_ID = 'L'
        self.CHAIN_ID = 'T'

        logging.getLogger("requests").setLevel(logging.WARNING)
        console = logging.StreamHandler()
        console.setLevel(logging.ERROR)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

        self.LTO = pyLTOCoin(self)

    def Account(self, address='', publicKey='', privateKey='', seed='', nonce=0):

        if seed:
            account = self.accountFactory.createFromSeed(seed, nonce)
        elif privateKey:
            account = self.accountFactory.createFromPrivateKey(privateKey)
        elif publicKey:
            account = self.accountFactory.createFromPublicKey(publicKey)
        else:
            account = self.accountFactory.create()

        # We don't have a case for someone who just passes the address
        if not self.accountFactory.assertAccount(account, address, publicKey, privateKey, seed):
            raise Exception("Account info are inconsistent")
        return account

    def throw_error(self, msg):
        if self.THROW_EXCEPTION_ON_ERROR:
            raise PyLTOException(msg)

    def setThrowOnError(self, throw=True):
        # global THROW_EXCEPTION_ON_ERROR
        self.THROW_EXCEPTION_ON_ERROR = throw

    def setOffline(self):
        # global OFFLINE
        self.OFFLINE = True

    def setOnline(self):
        # global OFFLINE
        self.OFFLINE = False

    def setChain(self, chain='', chain_id=None):
        # global CHAIN, CHAIN_ID
        if chain == '':
            chain = self.CHAIN

        if chain_id is not None:
            self.CHAIN = chain
            self.CHAIN_ID = chain_id
        else:
            if chain.lower() == 'mainnet' or chain.lower() == 'l':
                self.CHAIN = 'mainnet'
                self.CHAIN_ID = 'L'
            else:
                self.CHAIN = 'testnet'
                self.CHAIN_ID = 'T'

    def getChain(self):
        return self.CHAIN

    def getNode(self):
        return self.NODE


    def validateAddress(self, address):
        addr = crypto.bytes2str(base58.b58decode(address))
        if addr[0] != chr(self.ADDRESS_VERSION):
            logging.error("Wrong address version")
        elif addr[1] != self.CHAIN_ID:
            logging.error("Wrong chain id")
        elif len(addr) != self.ADDRESS_LENGTH:
            logging.error("Wrong address length")
        elif addr[-self.ADDRESS_CHECKSUM_LENGTH:] != crypto.hashChain(
                crypto.str2bytes(addr[:-self.ADDRESS_CHECKSUM_LENGTH]))[:self.ADDRESS_CHECKSUM_LENGTH]:

            logging.error("Wrong address checksum")
        else:

            return True
        return False


class PyLTOException(ValueError):
    pass
