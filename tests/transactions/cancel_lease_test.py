from lto.transactions.cancel_lease import CancelLease
from lto.accounts.account_factory_ed25519 import AccountFactoryED25519 as AccountFactory
from time import time
from unittest import mock
from lto import crypto
import pytest
from freezegun import freeze_time

class TestCancelLease:

    ACCOUNT_SEED = "df3dd6d884714288a39af0bd973a1771c9f00f168cf040d6abb6a50dd5e055d8"
    account = AccountFactory('T').create_from_seed(ACCOUNT_SEED)

    def test_construct(self):
        transaction = CancelLease('B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo')
        assert transaction.lease_id == 'B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo'
        assert transaction.tx_fee == 500000000


    @freeze_time("2021-01-14")
    def test_sign_with(self):
        transaction = CancelLease('3N3Cn2pYtqzj7N9pviSesNe8KG9Cmb718Y1')
        assert transaction.is_signed() is False
        transaction.sign_with(self.account)
        assert transaction.is_signed() is True
        timestamp = int(time() * 1000)
        assert str(transaction.timestamp)[:-3] == str(timestamp)[:-3]
        assert transaction.sender == '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2'
        assert transaction.sender_public_key == '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz'
        assert self.account.verify_signature(transaction.to_binary(), transaction.proofs[0])


    expected_v2 = {'fee': 500000000,
                'senderKeyType': 'ed25519',
                'leaseId': 'B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo',
                'proofs': ['4bvuZhr215hhxyBmyvbSoMMb2QHULuy36Zdsx2zY2dQqzowHYVq3S6g21J8TzHN5cdxVyChTMx3HMssyaWKAwNYF'],
                'sender': '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
                'senderPublicKey': '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
                'timestamp': 1326499200000,
                'type': 9,
                'version': 2}

    expected_v3 = {
            "type": 9,
            "version": 3,
            "sender": '3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2',
            "senderKeyType": "ed25519",
            "senderPublicKey": '4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz',
            "fee": 500000000,
            "timestamp": 1326499200000,
            "proofs": ['3mR62iT9JBuyDBic678DWaSW5wZ8mZv7dRDTc7LKdA4pu6rJAzFbAUDu3Mi7RjUirwvtryAErSwE37EatJZ1kUbP'],
            "leaseId": "B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo"
        }

    @freeze_time("2021-01-14")
    @pytest.mark.parametrize("version, expected", [(2, expected_v2), (3, expected_v3)])
    def test_to_json(self, expected, version):
        transaction = CancelLease('B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo')
        transaction.timestamp = 1326499200000
        transaction.version = version
        transaction.sign_with(self.account)
        assert transaction.to_json() == expected

    @mock.patch('src.lto.PublicNode')
    def test_broadcast(self, mock_Class):
        transaction = CancelLease('B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo')
        broadcastedTransaction = CancelLease('B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo')
        broadcastedTransaction.id = '7cCeL1qwd9i6u8NgMNsQjBPxVhrME2BbfZMT1DF9p4Yi'
        mc = mock_Class.return_value
        mc.broadcast.return_value = broadcastedTransaction
        assert mc.broadcast(transaction) == broadcastedTransaction


    @freeze_time("2021-01-14")
    def test_from_data(self):
        data = {
            "type": 9,
            "version": 3,
            "id": "BLMA4vkfe2S5UFHnoPyTh8SJmpTA1deh5SnWk1bdfjhq",
            "sender": "3MtHYnCkd3oFZr21yb2vEdngcSGXvuNNCq2",
            "senderKeyType": 'ed25519',
            "senderPublicKey": "4EcSxUkMxqxBEBUBL2oKz3ARVsbyRJTivWpNrYQGdguz",
            "timestamp": 1519862400,
            "fee": 500000000,
            "leaseId": "B22YzYdNv7DCqMqdK2ckpt53gQuYq2v997N7g8agZoHo",
            "proofs": [
                "2AKUBja93hF8AC2ee21m9AtedomXZNQG5J3FZMU85avjKF9B8CL45RWyXkXEeYb13r1AhpSzRvcudye39xggtDHv"
            ]
        }
        transaction = CancelLease(lease_id='').from_data(data)
        crypto.compare_data_transaction(data, transaction)



