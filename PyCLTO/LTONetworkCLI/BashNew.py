import argparse
from PyCLTO.Transactions import Transfer as Transf
from PyCLTO import PublicNode
from PyCLTO.Transactions.Lease import Lease
from PyCLTO.Transactions.Sponsor import Sponsor
from PyCLTO.Transactions.CancelSponsor import CancelSponsor
from Commands import Account
import ConfigNew
import HandleDefaultNew as handle

CHAIN_ID = 'L'
URL = 'https://testnet.lto.network'


def main():
    parser = argparse.ArgumentParser(description='LTO Network CLI client')
    parser.add_argument('list', type=str, nargs='+')
    parser.add_argument('--name', type=str, nargs=1)
    parser.add_argument('--hash', type=str, nargs=1)
    parser.add_argument('--recipient', type=str, nargs=1)
    parser.add_argument('--amount', type=int, nargs=1)
    parser.add_argument('--leaseId', type=str, nargs=1)
    parser.add_argument('--network', type=str, nargs=2)

    # args = parser.parse_args(['accounts', 'create', 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep', '--name', 'foobar'])
    # args = parser.parse_args(['transfer','--recipient', '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb','--amount', '200000000'])
    # args = parser.parse_args(['accounts','set-default', 'test'])
    # args = parser.parse_args(['anchor','--hash', 'e3b0c44298fc1c149afbf4c8946fb92417ae41e4649b934ca495981b7852b855'])
    # args = parser.parse_args(['association','issue', '--recipient', 'tonio', '--hash', 'cartonio'])
    # args = parser.parse_args(['lease','create', '--recipient', '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', '--amount', '300000000'])
    # args = parser.parse_args(['lease','cancel', '--leaseId', '939cfFmtJx6v7mG1xQVjcDH2dNzDdUpCTTyc8J4tBZ98'])
    # args = parser.parse_args(['set-node','--network','T', 'https://testnet.lto.network'])
    args = parser.parse_args(['set-node', '--network', 'T', 'https://testnet.lto.network'])
    print('args: ', args)
    processArgs(args, parser)




def Anchor(hash):
    print('loop here ? ')
    if not hash:
        raise Exception('No hash was passed')
    hash = hash[0]
    account = handle.getDefaultAccount(CHAIN_ID)
    transfer = Anchor(hash)
    transfer.signWith(account)
    url = 'https://testnet.lto.network'
    node = PublicNode(url)
    node.broadcast(transfer)
    print('ok')


def Transfer(recipient, amount):
    if not recipient:
        raise Exception('Recipient field must be fulled')
    recipient = recipient[0]
    if not amount:
        raise Exception('Amount field must be filled')
    amount = amount[0]

    account = handle.getDefaultAccount(CHAIN_ID)
    transfer = Transf.Transfer(recipient, int(amount))
    transfer.signWith(account)
    url = 'https://testnet.lto.network'
    node = PublicNode(url)
    node.broadcast(transfer)


def Association(args, recipient, hash):
    print(args)
    print(recipient)
    print(hash)
    if args[1] == 'issue':
        print('ok')
    elif args[1] == 'revoke':
        print('ok')
    else:
        raise Exception('Wrong association input')


def createLease(recipient, amount):
    transaction = Lease(recipient[0], amount[0])
    account = handle.getDefaultAccount(CHAIN_ID)
    transaction.signWith(account)
    returnValue = transaction.broadcastTo(PublicNode(URL))
    print(returnValue.leaseId)


def cancelLease(leaseId):
    print(leaseId)


def sponsorship(args, recipient):
    if args[1] == 'create':
        transaction = Sponsor(recipient[0])
        account = handle.getDefaultAccount(CHAIN_ID)
        transaction.signWith(account)
        returnValue = transaction.broadcastTo(PublicNode(URL))
    elif args[1] == 'cancel':
        transaction = CancelSponsor(recipient[0])
        account = handle.getDefaultAccount(CHAIN_ID)
        transaction.signWith(account)
        returnValue = transaction.broadcastTo(PublicNode(URL))

    else:
        raise Exception("Wrong Sponsorship syntax")


def processArgs(arguments, parser):
    args = arguments.list
    name = arguments.name
    hash = arguments.hash
    recipient = arguments.recipient
    amount = arguments.amount
    leaseId = arguments.leaseId
    network = arguments.network

    if name:
        name = name[0]

    if args[0] == 'accounts':
        Account.func(args, name, network)

    elif args[0] == 'anchor':
        Anchor(hash)
    elif args[0] == 'transfer':
        Transfer(recipient, amount)
    elif args[0] == 'association':
        if not recipient or not hash or args[1] not in ['issue', 'revoke']:
            parser.error('Incorrect association syntax')
        Association(args, recipient, hash)
    elif args[0] == 'lease':
        if args[1] == 'create':
            if not recipient or not amount:
                parser.error('Incorrect lease syntax')
            else:
                createLease(recipient, amount)
        elif args[1] == 'cancel':
            if not leaseId:
                parser.error('Incorrect lease syntax')
            else:
                cancelLease(leaseId)
        else:
            parser.error('Incorrect lease syntax')

    elif args[0] == 'sponsorship':
        if (args[1] not in ['create', 'cancel']) or not recipient:
            parser.error('Invalid sponsorhip syntax')
        else:
            sponsorship(args, recipient)

    elif args[0] == 'set-node':
        ConfigNew.setnode(network)
    else:
        parser.error('Unrecognized input')


if __name__ == '__main__':
    main()


