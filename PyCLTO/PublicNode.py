import requests
import json


class PublicNode(object):
    def __init__(self, url):
        self.url = url

        ''' is the offline important? it should be imported from the init.py'''


    def wrapper(self, api, postData='', host='', headers=''):

        if not host:
            host = self.url

        if postData:
            req = requests.post('%s%s' % (host, api), data=postData,
                                headers={'content-type': 'application/json'}).json()
        else:
            req = requests.get('%s%s' % (host, api), headers=headers).json()
        return req

    def broadcast(self, transaction):
        data = json.dumps(transaction.toJson())
        return self.wrapper('/transactions/broadcast', data)

    def height(self):
        return self.wrapper('/blocks/height')['height']

    def lastblock(self):
        return self.wrapper('/blocks/last')

    def block(self, n):
        return self.wrapper('/blocks/at/%d' % n)

    def tx(self, id):
        return self.wrapper('/transactions/info/%s' % id)



    def balance(self, address):
        # check if this is an account type
        # technically it was address

        # address = type(account) == Account ? account.address : account

        try:
            return self.wrapper('/addresses/balance/%s' % address)['balance']
        except:
            return -1

    def transactions(self, limit=100, after='', address = ''):
        return self.wrapper('/transactions/address/%s/limit/%d%s' % (
            address, limit, "" if after == "" else "?after={}".format(after)))

#url = 'https://testnet.lto.network'
#address = '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du'
# node = PublicNode(url)
# node.tx('T')

#node = PublicNode(url)
#print(node.balance(address))