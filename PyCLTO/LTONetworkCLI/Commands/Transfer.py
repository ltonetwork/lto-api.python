import PyCLTO.LTONetworkCLI.HandleDefaultNew as handle
from PyCLTO.Transactions.Transfer import Transfer


def func(recipient, amount):
    if not recipient:
        raise Exception('Recipient field must be filled')
    recipient = recipient[0]
    if not amount:
        raise Exception('Amount filled must be filled')
    amount = amount[0]

    transaction = Transfer(recipient, int(amount))
    transaction.signWith(handle.getAccount())
    transaction.broadcastTo(handle.getNode())
