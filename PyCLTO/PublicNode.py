import requests
import json

from PyCLTO import Account
import PyCLTO

class PublicNode(object):
    def __init__(self, url):
        self.url = url


    def wrapper(self, api, postData='', host='', headers=''):
        if not host:
            host = self.url

        if postData:
            req = requests.post('%s%s' % (host, api), data=postData,
                                headers={'content-type': 'application/json'}).json()
        else:
            req = requests.get('%s%s' % (host, api), headers=headers).json()

        # Check error

        return req

    def broadcast(self, transaction):
        data = json.dumps(transaction.toJson())
        #return self.wrapper('/transactions/broadcast', data)
        response = self.wrapper('/transactions/broadcast', data)
        print(response)
        print(response['recipient'])
        return PyCLTO.PyCLTO().fromData(response)

    def getScript(self, scriptSource):
        return self.wrapper('/utils/script/compile', scriptSource)['script'][7:]


    def height(self):
        return self.wrapper('/blocks/height')['height']

    def lastblock(self):
        return self.wrapper('/blocks/last')

    def block(self, n):
        return self.wrapper('/blocks/at/%d' % n)

    def tx(self, id):
        response = self.wrapper('/transactions/info/%s' % id)
        return PyCLTO.PyCLTO().fromData(response)


    def balance(self, address):
        # check if this is an account type
        # technically it was address

        if type(address) == Account:
            address = address.address

        try:
            return self.wrapper('/addresses/balance/%s' % address)['balance']
        except:
            return -1

    def transactions(self, limit=100, after='', address = ''):
        return self.wrapper('/transactions/address/%s/limit/%d%s' % (
            address, limit, "" if after == "" else "?after={}".format(after)))

