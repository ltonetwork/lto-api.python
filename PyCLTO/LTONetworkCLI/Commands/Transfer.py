import PyCLTO.LTONetworkCLI.HandleDefaultNew as handle
from PyCLTO.Transactions.Transfer import Transfer


def func(recipient, amount):
    if not recipient or not amount:
        raise Exception('Incorrect transfer syntax')

    recipient = recipient[0]
    amount= amount[0]

    transaction = Transfer(recipient, amount)
    transaction.signWith(handle.getAccount())
    transaction.broadcastTo(handle.getNode())
