import requests
import json
from urllib.parse import urlencode
from lto.transactions import from_data as tx_from_data, SetScript
from lto.accounts import Account


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
            r = requests.post('{}{}'.format(host, endpoint), data=post_data,
                              headers={**headers, 'content-type': 'application/json'})
        else:
            r = requests.get('{}{}'.format(host, endpoint), headers=headers)

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
        response = self.request('/transactions/broadcast', post_data=data)
        return tx_from_data(response)

    def compile(self, script_source):
        compiled_script = self.request('/utils/script/compile', post_data=script_source)['script']
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
        return self.request('/leasing/active/{}'.format(self.__addr(address)))

    def data(self, address):
        data = self.request('/addresses/data/{}'.format(self.__addr(address)))
        return {entry['key']: entry['value'] for entry in data}

    def data_by_key(self, address, key):
        entry = self.request('/addresses/data/{}/{}'.format(self.__addr(address), key))
        return entry["value"] if entry else None

    def sponsorship_list(self, address):
        return self.request('/sponsorship/status/{}'.format(self.__addr(address)))

    def association_list(self, address):
        return self.request('/associations/status/{}'.format(self.__addr(address)))

    def node_status(self):
        return self.request('/node/status')

    def balance(self, address):
        return self.request('/addresses/balance/{}'.format(self.__addr(address)))['balance']

    def balance_details(self, address):
        return self.request('/addresses/balance/details/{}'.format(self.__addr(address)))

    def validate_address(self, address):
        return self.request('/addresses/validate/{}'.format(address))['valid']

    def transactions(self, address, tx_type=None, limit=None, after=None):
        items = ([('type', t) for t in tx_type] if type(tx_type) == list else [('type', tx_type)]) +\
                [('limit', limit), ('after', after)]
        query = urlencode([(k, v) for k, v in items if v is not None])
        txs_data = self.request('/transactions/address/{}?{}'.format(self.__addr(address), query))[0]
        return [tx_from_data(tx_data) for tx_data in txs_data]

    def sign_transaction(self, transaction):
        data = json.dumps(transaction.to_json())
        return self.request('/transactions/sign', post_data=data)
