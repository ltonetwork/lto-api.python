from lto.transactions.anchor import Anchor
from lto.transactions.lease import Lease
from lto.transactions.association import Association
from lto.transactions.cancel_lease import CancelLease
from lto.transactions.cancel_sponsorship import CancelSponsorship
from lto.transactions.mass_transfer import MassTransfer
from lto.transactions.revoke_association import RevokeAssociation
from lto.transactions.set_script import SetScript
from lto.transactions.sponsorship import Sponsorship
from lto.transactions.transfer import Transfer
from lto.transactions.register import Register
from lto.transactions.data import Data
from lto.transactions.burn import Burn

def from_data(data):
    if data['type'] == 4:
        return Transfer.from_data(data)
    elif data['type'] == 8:
        return Lease.from_data(data)
    elif data['type'] == 9:
        return CancelLease.from_data(data)
    elif data['type'] == 11:
        return MassTransfer.from_data(data)
    elif data['type'] == 12:
        return Data.from_data(data)
    elif data['type'] == 13:
        return SetScript.from_data(data)
    elif data['type'] == 15:
        return Anchor.from_data(data)
    elif data['type'] == 16:
        return Association.from_data(data)
    elif data['type'] == 17:
        return RevokeAssociation.from_data(data)
    elif data['type'] == 18:
        return Sponsorship.from_data(data)
    elif data['type'] == 19:
        return CancelSponsorship.from_data(data)
    elif data['type'] == 20:
        return Register.from_data(data)
    elif data['type'] == 21:
        return Burn.from_data(data)
    else:
        raise Exception('Incorrect transaction Type')
