import base58
from lto import crypto
from lto.accounts.account import Account
from lto.transaction import Transaction
import struct


class Register(Transaction):
    TYPE = 20
    BASE_FEE = 25000000
    VAR_FEE = 10000000
    DEFAULT_VERSION = 3

    def __init__(self, *accounts):
        super().__init__()

        self.accounts = list(map(self.__account_dict, accounts))
                
        self.tx_fee = self.BASE_FEE + len(self.accounts) * self.VAR_FEE
        self.version = self.DEFAULT_VERSION

        if len(self.accounts) > 100:
            raise Exception('Too many accounts')

    @staticmethod
    def __account_dict(account):
      return {'key_type': account.key_type, 'public_key': account.get_public_key()} \
          if isinstance(account, Account) else account

    def __accounts_data(self):
        data = b''
        
        for account in self.accounts:
            data += crypto.key_type_id(account['key_type'])
            data += base58.b58decode(account['public_key'])
        
        return data
    
    def __to_binary_v3(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                struct.pack(">H", len(self.accounts)) +
                self.__accounts_data())

    def to_binary(self):
        if self.version == 3:
            return self.__to_binary_v3()
        else:
            raise Exception('Incorrect Version ' + self.version)

    @staticmethod
    def __account_to_json(account):
        return {'keyType': account['key_type'], 'publicKey': account['public_key']}

    def to_json(self):
        return (crypto.merge_dicts({
            "id": self.id if self.id else "",
            "type": self.TYPE,
            "version": self.version,
            "sender": self.sender,
            "senderKeyType": self.sender_key_type,
            "senderPublicKey": self.sender_public_key,
            "fee": self.tx_fee,
            "timestamp": self.timestamp,
            "accounts": list(map(self.__account_to_json, self.accounts)),
            "proofs": self.proofs,
            "height": self.height if self.height else ""
            },
            self._sponsor_json()))

    @staticmethod
    def __account_from_data(data):
        return {'keyType': data['keyType'], 'publicKey': data['publicKey']}

    @staticmethod
    def from_data(data):
        tx = Register("")
        tx.id = data['id'] if 'id' in data else ''
        tx.type = data['type']
        tx.version = data['version']
        tx.sender = data['sender'] if 'sender' in data else ''
        tx.sender_key_type = data['senderKeyType'] if 'senderKeyType' in data else 'ed25519'
        tx.sender_public_key = data['senderPublicKey']
        tx.fee = data['fee']
        tx.timestamp = data['timestamp']
        tx.accounts = list(map(Register.__account_from_data, data['accounts']))
        tx.proofs = data['proofs'] if 'proofs' in data else []
        tx.height = data['height'] if 'height' in data else ''
        return tx

