from __future__ import absolute_import, division, print_function, unicode_literals

import AccountFactory
import PyCLTO.PublicNode
import PyCLTO.Transaction
import PyCLTO.Account
import PyCLTO.coin



class PyCLTO:

    def __init__(self, chainId='T'):
        self.accountFactory = AccountFactory.AccountFactory(chainId)

        if chainId == 'T':
            self.NODE = PublicNode.PublicNode('https://testnet.lto.network')
            self.CHAIN = 'testnet'
            self.CHAIN_ID = 'T'
        elif chainId == 'L':
            self.NODE = PublicNode.PublicNode('https://nodes.lto.network')
            self.CHAIN = 'mainnet'
            self.CHAIN_ID = 'L'
        else:
            self.NODE = ''

        # is this necessary ?
        self.LTO = coin.pyLTOCoin(self)

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

    def getChainId(self):
        return self.accountFactory.chainId

    def transaction(self, data):
        return Transaction.Transaction().fromData(data)
