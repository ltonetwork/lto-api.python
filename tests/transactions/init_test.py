from unittest import mock
import pytest
from lto.transactions import *


def get_data():
    set = {
        4: Transfer,
        8: Lease,
        9: CancelLease,
        11: MassTransfer,
        12: Data,
        13: SetScript,
        15: Anchor,
        16: Association,
        17: RevokeAssociation,
        18: Sponsorship,
        19: CancelSponsorship,
        20: Register
    }
    for type in set:
        yield type, set[type]

class TestInit:
    @pytest.mark.parametrize("type,tx_class", get_data())
    def test_from_data(self, type, tx_class):
        data = {'type': type}
        with mock.patch.object(tx_class, "from_data"):
            from_data(data)

    def test_from_data_unknown_type(self):
        data = {'type': 999}
        with pytest.raises(Exception):
            from_data(data)
