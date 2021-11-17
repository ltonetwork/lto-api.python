import requests
import json

from lto.account import Account


class PublicNode(object):
    def __init__(self, url, api_key=''):
        self.url = url
        self.api_key = api_key

    def wrapper(self, api, post_data='', host='', headers=None):
        if headers is None:
            headers = {}

        if not host:
            host = self.url

        if self.api_key:
            headers = {"X-API-Key": self.api_key}

        if post_data:
            r = requests.post('%s%s' % (host, api), data=post_data,
                              headers=headers | {'content-type': 'application/json'})
        else:
            r = requests.get('%s%s' % (host, api), headers=headers)

        if r.status_code != 200:
            json_resp = json.loads(r.text)
            raise Exception('{}'.format(json_resp['message']))

        r.raise_for_status()

        return r.json()

    def broadcast(self, transaction):
        from lto import PyCLTO
        data = json.dumps(transaction.to_json())
        response = self.wrapper(api='/transactions/broadcast', post_data=data)
        return PyCLTO().from_data(response)

    def compile(self, script_source):
        return self.wrapper(api='/utils/script/compile', post_data=script_source)['script']

    def height(self):
        return self.wrapper('/blocks/height')['height']

    def last_block(self):
        return self.wrapper('/blocks/last')

    def block(self, n):
        return self.wrapper('/blocks/at/%d' % n)

    def tx(self, id):
        from lto import PyCLTO
        response = self.wrapper('/transactions/info/%s' % id)
        return PyCLTO().from_data(response)

    def lease_list(self, address):
        return self.wrapper(api='/leasing/active/{}'.format(address))

    def sponsorship_list(self, address):
        return self.wrapper(api='/sponsorship/status/{}'.format(address))

    def balance(self, address):

        if type(address) == Account:
            address = address.address

        try:
            return self.wrapper('/addresses/balance/%s' % address)['balance']
        except:
            return -1

    def transactions(self, limit=100, after='', address=''):
        return self.wrapper('/transactions/address/%s/limit/%d%s' % (
            address, limit, "" if after == "" else "?after={}".format(after)))

    def sign_transaction(self, transaction):
        data = json.dumps(transaction.to_json())
        return(self.wrapper(api='/transactions/sign', post_data=data))

