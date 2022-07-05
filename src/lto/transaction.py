from abc import ABC, abstractmethod
from time import time
import base58
from nacl.signing import VerifyKey


class Transaction(ABC):

    def __init__(self):
        self.id = None
        self.tx_fee = None
        self.timestamp = None
        self.sender = None
        self.sender_key_type = None
        self.sender_public_key = None
        self.sponsor = None
        self.sponsor_key_type = None
        self.sponsor_public_key = None
        self.chain_id = None
        self.proofs = []
        self.height = None

    @abstractmethod
    def to_binary(self):
        pass

    def is_signed(self):
        return len(self.proofs) != 0

    def sign_with(self, account):
        if self.timestamp is None:
            self.timestamp = int(time() * 1000)

        if self.sender is None:
            self.sender = account.address
            self.sender_key_type = account.key_type
            self.sender_public_key = account.get_public_key()
            
        if self.chain_id is None:
            self.chain_id = account.get_network()
        
        self.proofs.append(account.sign(self.to_binary()))

    def sponsor_with(self, sponsor_account):
        if not self.is_signed():
            raise Exception('Transaction must be signed first')

        self.sponsor = sponsor_account.address
        self.sponsor_public_key = sponsor_account.get_public_key()
        self.sponsor_key_type = sponsor_account.key_type
        self.proofs.append(sponsor_account.sign(self.to_binary()))

    def broadcast_to(self, node):
        return node.broadcast(self)

    @abstractmethod
    def to_json(self):
        pass

