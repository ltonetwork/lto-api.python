from PyCLTO.LTONetworkCLI import HandleDefaultNew as handle
from PyCLTO.Transactions.Lease import Lease
from PyCLTO.Transactions.CancelLease import CancelLease

def func(args, recipient, amount, leaseId):
    if args[1] not in ['create', 'cancel']:
        raise Exception('Wrong leasing syntax')

    if args[1] == 'create':
        if not recipient or not amount:
            raise Exception('Wrong create lease syntax')
        recipient = recipient[0]
        amount = amount[0]
        transaction = Lease(recipient=recipient, amount=amount)
        transaction.signWith(handle.getAccount())
        transaction.broadcastTo(handle.getNode())
    else:
        # cancel case
        if not leaseId:
            raise Exception('Wrong cancel lease syntax')
        leaseId = leaseId[0]
        transaction = CancelLease(leaseId=leaseId)
        transaction.signWith(handle.getAccount())
        transaction.broadcastTo(handle.getNode())