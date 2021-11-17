from abc import ABC, abstractmethod
from time import time
from lto.public_node import PublicNode
import base58
from nacl.signing import VerifyKey


class Transaction(ABC):

    def __init__(self):
        self.tx_fee = 0
        self.timestamp = 0
        self.proofs = []
        self.sender = ''
        self.sender_public_key = ''
        self.chain_id = ''
        self.sponsor = ''
        self.sponsor_public_key = ''
        self.sender_key_type = 'ed25519'
        self.sponsor_key_type = 'ed25519'

    @abstractmethod
    def to_binary(self):
        pass

    def is_signed(self):
        return len(self.proofs) != 0

    def sign_with(self, account):
        if self.timestamp == 0:
            self.timestamp = int(time() * 1000)

        if self.sender == '':
            self.sender = account.address
            self.sender_public_key = account.get_public_key()

        self.chain_id = account.get_network()
        self.sender_key_type = account.key_type

        self.proofs.append(account.sign(self.to_binary()))

    def sponsor_with(self, sponsor_account):
        if not self.is_signed():
            raise Exception('Transaction must be signed first')

        self.sponsor = sponsor_account.address
        self.sponsor_public_key = sponsor_account.public_key
        self.proofs.append(sponsor_account.sign(self.to_binary()))

    def broadcast_to(self, node: PublicNode):
        return node.broadcast(self)

    @abstractmethod
    def to_json(self):
        pass

    def _sponsor_json(self):
        if self.sponsor:
            return {"sponsor": self.sponsor,
                    "sponsorPublicKey": base58.b58encode(self.sponsor_public_key.__bytes__()),
                    "sponsorKeyType": self.sponsor_key_type}
        else:
            return{}

    def __getattr__(self, item):
        return getattr(self, item)
