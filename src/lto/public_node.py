import requests
import json

from lto.transactions import from_data as tx_from_data
from lto.transactions.set_script import SetScript
from lto.accounts.account import Account
from lto import crypto


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
                              headers=crypto.merge_dicts(headers, {'content-type': 'application/json'}))
        else:
            r = requests.get('%s%s' % (host, api), headers=headers)

        if r.status_code != 200:
            method = 'POST' if post_data else 'GET'
            json_resp = json.loads(r.text)
            raise Exception(
                '{} {}{} responded with {} {}'.format(method, host, api, r.status_code, r.reason),
                json_resp
            )

        r.raise_for_status()

        return r.json()

    def broadcast(self, transaction):
        data = json.dumps(transaction.to_json())
        response = self.wrapper(api='/transactions/broadcast', post_data=data)
        return tx_from_data(response)

    def compile(self, script_source):
        compiled_script = self.wrapper(api='/utils/script/compile', post_data=script_source)['script']
        return SetScript(compiled_script)

    def height(self):
        return self.wrapper('/blocks/height')['height']

    def last_block(self):
        return self.wrapper('/blocks/last')

    def block(self, n):
        return self.wrapper('/blocks/at/%d' % n)

    def tx(self, id):
        response = self.wrapper('/transactions/info/%s' % id)
        return tx_from_data(response)

    def lease_list(self, address):
        return self.wrapper(api='/leasing/active/{}'.format(address))

    def sponsorship_list(self, address):
        return self.wrapper(api='/sponsorship/status/{}'.format(address))

    def association_list(self, address):
        return self.wrapper(api='/associations/status/{}'.format(address))

    def node_status(self):
        return self.wrapper(api='/node/status')

    def balance(self, address):

        if type(address) == Account:
            address = address.address

        try:
            return self.wrapper('/addresses/balance/%s' % address)['balance']
        except:
            return -1

    def balance_details(self, address):
        if type(address) == Account:
            address = address.address
        return self.wrapper('/addresses/balance/details/%s' % address)


    def transactions(self, limit=100, after='', address=''):
        return self.wrapper('/transactions/address/%s/limit/%d%s' % (
            address, limit, "" if after == "" else "?after={}".format(after)))

    def sign_transaction(self, transaction):
        data = json.dumps(transaction.to_json())
        return(self.wrapper(api='/transactions/sign', post_data=data))

