import argparse
import ConfigNew

from Commands import Account
from Commands import Transfer
from Commands import Anchor
from Commands import Association
from Commands import Leasing
from Commands import Sponsorhip

# URL = 'https://testnet.lto.network'
# URL = 'https://nodes.lto.network'
# CHAIN_ID = 'L'



def main():
    parser = argparse.ArgumentParser(description='LTO Network CLI client')
    parser.add_argument('list', type=str, nargs='+')
    parser.add_argument('--name', type=str, nargs=1)
    parser.add_argument('--hash', type=str, nargs=1)
    parser.add_argument('--recipient', type=str, nargs=1)
    parser.add_argument('--amount', type=int, nargs=1)
    parser.add_argument('--leaseId', type=str, nargs=1)
    parser.add_argument('--network', type=str, nargs=2)
    parser.add_argument('--type', type=int, nargs=1)

    # args = parser.parse_args(['accounts', 'create', 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep', '--name', 'foobar'])
    #args = parser.parse_args(['transfer','--recipient', '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj','--amount', '200000000'])
    # args = parser.parse_args(['accounts','set-default', 'test'])
    # args = parser.parse_args(['anchor','--hash', 'e3b0c44298fc1c149afbf4c8946fb92417ae41e4649b934ca495981b7852b855'])
    # args = parser.parse_args(['association','revoke', '--recipient', '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', '--associationType', '3', '--hash', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'])
    #args = parser.parse_args(['lease','create', '--recipient', '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', '--amount', '300000000'])
    # args = parser.parse_args(['lease','cancel', '--leaseId', '939cfFmtJx6v7mG1xQVjcDH2dNzDdUpCTTyc8J4tBZ98'])
    # args = parser.parse_args(['set-node','--network','T', 'https://testnet.lto.network'])
    # args = parser.parse_args(['set-node', '--network', 'T', 'https://testnet.lto.network'])
    args = parser.parse_args(['accounts', 'create'])
    print('args: ', args)
    processArgs(args, parser)

    # fro the transactions, it takes the chainId and url from the config.ini if presents,
    # otherwise it uses the default.
    # I could use an account on mainnet, set defualt on testnet and get an error
    # should we avoid this kind of circumstance ?
    # - - - - - - - - - - - - - - - - - - - - - - -
    # How to set the same default URL for all the files ?
    # - - - - - - - - - - - - - - - - - - - - - - -
    # Cannot get an input for ex mass transfer
    # - - - - - - - - - - - - - - - - - - - - - - -


def processArgs(arguments, parser):
    args             = arguments.list
    name             = arguments.name
    hash             = arguments.hash
    recipient        = arguments.recipient
    amount           = arguments.amount
    leaseId          = arguments.leaseId
    network          = arguments.network
    type             = arguments.type


    if name:
        name = name[0]

    if args[0] == 'accounts':
        Account.func(args, name, network)
    elif args[0] == 'anchor':
        Anchor.func(hash)
    elif args[0] == 'transfer':
        Transfer.func(recipient, amount)
    elif args[0] == 'association':
        Association.func(args, type, recipient, hash)
    elif args[0] == 'lease':
        Leasing.func(args, recipient, amount, leaseId)
    elif args[0] == 'sponsorship':
        Sponsorhip.func(args, recipient)
    elif args[0] == 'set-node':
        ConfigNew.setnode(network)
    else:
        parser.error('Unrecognized input')


if __name__ == '__main__':
    main()