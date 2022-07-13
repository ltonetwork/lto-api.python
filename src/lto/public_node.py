import requests
import json
from urllib.parse import urlencode
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

    def request(self, endpoint, post_data='', host='', headers=None):
        if headers is None:
            headers = {}

        if not host:
            host = self.url

        if self.api_key:
            headers = {"X-API-Key": self.api_key}

        if post_data:
            r = requests.post('%s%s' % (host, endpoint), data=post_data,
                              headers=crypto.merge_dicts(headers, {'content-type': 'application/json'}))
        else:
            r = requests.get('%s%s' % (host, endpoint), headers=headers)

        if r.status_code != 200:
            method = 'POST' if post_data else 'GET'
            try:
                error = json.loads(r.text)
            except:
                error = r.text

            raise Exception(
                '{} {}{} responded with {} {}'.format(method, host, endpoint, r.status_code, r.reason),
                error
            )

        r.raise_for_status()

        return r.json()

    def broadcast(self, transaction):
        data = json.dumps(transaction.to_json())
        response = self.request(endpoint='/transactions/broadcast', post_data=data)
        return tx_from_data(response)

    def compile(self, script_source):
        compiled_script = self.request(endpoint='/utils/script/compile', post_data=script_source)['script']
        return SetScript(compiled_script)

    def height(self):
        return self.request('/blocks/height')['height']

    def last_block(self):
        return self.request('/blocks/last')

    def block(self, height):
        return self.request('/blocks/at/{}'.format(height))

    def tx(self, id):
        response = self.request('/transactions/info/{}'.format(id))
        return tx_from_data(response)

    def lease_list(self, address):
        return self.request(endpoint='/leasing/active/{}'.format(self.__addr(address)))

    def data(self, address):
        data = self.request('/addresses/data/{}'.format(self.__addr(address)))
        return {entry['key']: entry['value'] for entry in data}

    def data_by_key(self, address, key):
        entry = self.request(endpoint='/addresses/data/{}/{}'.format(self.__addr(address), key))
        return entry["value"] if entry else None

    def sponsorship_list(self, address):
        return self.request(endpoint='/sponsorship/status/{}'.format(self.__addr(address)))

    def association_list(self, address):
        return self.request(endpoint='/associations/status/{}'.format(self.__addr(address)))

    def node_status(self):
        return self.request(endpoint='/node/status')

    def balance(self, address):
        return self.request('/addresses/balance/%s' % self.__addr(address))['balance']

    def balance_details(self, address):
        return self.request('/addresses/balance/details/%s' % self.__addr(address))

    def validate_address(self, address):
        return self.request('/addresses/validate/{}'.format(address))['valid']

    def transactions(self, address, type=None, limit=None, after=None):
        query = urlencode({k: v for k, v in {"type": type, "limit": limit, "after": after}.items() if v is not None})
        return self.request('/transactions/address/{}?{}'.format(self.__addr(address), query))

    def sign_transaction(self, transaction):
        data = json.dumps(transaction.to_json())
        return self.request(endpoint='/transactions/sign', post_data=data)
