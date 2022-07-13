import base58
from lto import crypto
import struct
from lto.transaction import Transaction


class CancelSponsorship(Transaction):
    BASE_FEE = 500000000
    TYPE = 19
    DEFAULT_VERSION = 3

    def __init__(self, recipient: str):
        super().__init__()
        self.recipient = recipient
        crypto.validate_address(recipient)
        self.tx_fee = self.BASE_FEE
        self.version = self.DEFAULT_VERSION

    def __to_binary_v1(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\1' +
                crypto.str2bytes(crypto.get_network(self.sender)) +
                base58.b58decode(self.sender_public_key) +
                base58.b58decode(self.recipient) +
                struct.pack(">Q", self.timestamp) +
                struct.pack(">Q", self.tx_fee))

    def __to_binary_v3(self):
        return (self.TYPE.to_bytes(1, 'big') +
                b'\3' +
                crypto.str2bytes(self.chain_id) +
                struct.pack(">Q", self.timestamp) +
                crypto.key_type_id(self.sender_key_type) +
                base58.b58decode(self.sender_public_key) +
                struct.pack(">Q", self.tx_fee) +
                base58.b58decode(self.recipient))

    def to_binary(self):
        if self.version == 1:
            return self.__to_binary_v1()
        elif self.version == 3:
            return self.__to_binary_v3()
        else:
            raise Exception('Incorrect Version')

    def to_json(self):
        return crypto.clean_dict({
            "id": self.id,
            "type": self.TYPE,
            "version": self.version,
            "senderKeyType": self.sender_key_type,
            "recipient": self.recipient,
            "sender": self.sender,
            "senderPublicKey": self.sender_public_key,
            "timestamp": self.timestamp,
            "fee": self.tx_fee,
            "sponsor": self.sponsor,
            "sponsorKeyType": self.sponsor_key_type,
            "sponsorPublicKey": self.sponsor_public_key,
            "proofs": self.proofs or None,
            "height": self.height
        })

    @staticmethod
    def from_data(data):
        tx = CancelSponsorship(data['recipient'])
        tx._init_from_data(data)

        return tx

