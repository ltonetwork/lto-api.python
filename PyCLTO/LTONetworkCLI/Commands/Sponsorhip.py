from PyCLTO.LTONetworkCLI import HandleDefaultNew as handle
from PyCLTO.Transactions.Sponsor import Sponsor
from PyCLTO.Transactions.CancelSponsor import CancelSponsor

def func(args, recipient):
    if args[1] not in ['create', 'cancel'] and not recipient:
        raise Exception('Invalid Sponsorship syntax')

    recipient = recipient[0]

    if args[1] == 'create':
        transaction = Sponsor(recipient)
        transaction.signWith(handle.getAccount())
        transaction.broadcastTo(handle.getNode())
    else:
        # cancel case
        transaction = CancelSponsor(recipient)
        transaction.signWith(handle.getAccount())
        transaction.broadcastTo(handle.getNode())