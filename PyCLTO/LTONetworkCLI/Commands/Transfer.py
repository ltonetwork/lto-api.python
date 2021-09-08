import configparser
import PyCLTO.LTONetworkCLI.HandleDefaultNew as handle
from PyCLTO.Transactions.Transfer import Transfer
from PyCLTO.PublicNode import PublicNode


def func(recipient, amount):
    if not recipient:
        raise Exception('Recipient field must be filled')
    recipient = recipient[0]
    if not amount:
        raise Exception('Amount filled must be filled')
    amount = amount[0]

    config = configparser.ConfigParser()
    config.read('L/config.ini')
    if 'Default' not in config.sections():
        raise Exception ('No Default account set')
    address = config.get('Default', 'account')
    account = handle.getAccount(address, config)

    if 'Node' in config.sections():
        URL = config.get('Node', 'url')
    else:
        URL = 'https://nodes.lto.network'

    transaction = Transfer(recipient, int(amount))
    transaction.signWith(account)
    transaction.broadcastTo(PublicNode(URL))
