import requests
import json

from lto.transactions import from_data as tx_from_data, SetScript
from lto.accounts import Account
from lto import crypto


class PublicNode(object):
    def __init__(self, url, api_key=''):
        self.url = url
        self.api_key = api_key
        
    @staticmethod
    def __addr(account_or_address):
        return account_or_address.address if isinstance(account_or_address, Account) else account_or_address

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
            try:
                error = json.loads(r.text)
            except:
                error = r.text
            
            raise Exception(
                '{} {}{} responded with {} {}'.format(method, host, api, r.status_code, r.reason),
                error
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
        return self.wrapper(api='/leasing/active/{}'.format(self.__addr(address)))

    def get_data(self, address):
        return self.wrapper(api='/addresses/data/{}'.format(self.__addr(address)))

    def get_data_by_key(self, address, key):
        return self.wrapper(api='/addresses/data/{}/{}'.format(self.__addr(address), key))

    def sponsorship_list(self, address):
        return self.wrapper(api='/sponsorship/status/{}'.format(self.__addr(address)))

    def association_list(self, address):
        return self.wrapper(api='/associations/status/{}'.format(self.__addr(address)))

    def node_status(self):
        return self.wrapper(api='/node/status')

    def balance(self, address):
        try:
            return self.wrapper('/addresses/balance/%s' % self.__addr(address))['balance']
        except:
            return -1

    def balance_details(self, address):
        return self.wrapper('/addresses/balance/details/%s' % self.__addr(address))

    def validate_address(self, address):
        return self.wrapper('/addresses/validate/{}'.format(address))['valid']


    def data_of(self, address):
        data = self.wrapper('/addresses/data/%s' % self.__addr(address))
        dict = {}
        for entry in data:
            dict[entry['key']] = entry['value']
        return dict

    def transactions(self, address, limit=100, after=''):
        return self.wrapper('/transactions/address/%s/limit/%d%s' % (
            self.__addr(address), limit, "" if after == "" else "?after={}".format(after)))

    def sign_transaction(self, transaction):
        data = json.dumps(transaction.to_json())
        return(self.wrapper(api='/transactions/sign', post_data=data))

