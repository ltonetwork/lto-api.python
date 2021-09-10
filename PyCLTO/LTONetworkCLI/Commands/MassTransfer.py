from PyCLTO.Transactions.MassTransferLto import MassTransferLTO
import PyCLTO.LTONetworkCLI.HandleDefaultNew as handle


def func(stdin):
    if stdin == []:
        raise Exception("Transfers not present")

    transfers = processInput(stdin)
    transaction = MassTransferLTO(transfers)
    transaction.signWith(handle.getAccount())
    transaction.broadcastTo(handle.getNode())


def processInput(stdin):
    transfers = []
    for x in stdin:
        recipient, amount = x.split(':')
        transfers.append({'recipient': recipient, 'amount': int(amount)})
    return transfers