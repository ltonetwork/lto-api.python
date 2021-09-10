import argparse
import sys
import ConfigNew

from Commands import Account
from Commands import Transfer
from Commands import Anchor
from Commands import Association
from Commands import Leasing
from Commands import Sponsorhip
from Commands import MassTransfer

# URL = 'https://testnet.lto.network'
# URL = 'https://nodes.lto.network'
# CHAIN_ID = 'L'

# IF ERROR MODULE NOT FOUND:
# export PYTHONPATH=$PYTHONPATH:'pwd.../lto-api.python'


def main():
    parser = argparse.ArgumentParser(description='LTO Network CLI client')
    parser.add_argument('list', type=str, nargs='+')
    parser.add_argument('--name', type=str, nargs=1)
    parser.add_argument('--hash', type=str, nargs=1)
    parser.add_argument('--recipient', type=str, nargs=1)
    parser.add_argument('--amount', type=int, nargs=1)
    parser.add_argument('--leaseId', type=str, nargs=1)
    parser.add_argument('--network', type=str, nargs=1)
    parser.add_argument('--type', type=int, nargs=1)
    parser.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin)

    #args = parser.parse_args(['accounts', 'seed', '--name', 'main', '--network', 'T'])
    #args = parser.parse_args(['transfer','--recipient', '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj','--amount', '200000000'])
    #args = parser.parse_args(['accounts','set-default', 'main'])
    # args = parser.parse_args(['anchor','--hash', 'e3b0c44298fc1c149afbf4c8946fb92417ae41e4649b934ca495981b7852b855'])
    # args = parser.parse_args(['association','revoke', '--recipient', '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', '--associationType', '3', '--hash', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'])
    #args = parser.parse_args(['lease','create', '--recipient', '3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj', '--amount', '300000000'])
    # args = parser.parse_args(['lease','cancel', '--leaseId', '939cfFmtJx6v7mG1xQVjcDH2dNzDdUpCTTyc8J4tBZ98'])
    # args = parser.parse_args(['set-node','--network','T', 'https://testnet.lto.network'])
    #args = parser.parse_args(['set-node',  'https://testnet.lto.network','--network', 'T',])
    args = parser.parse_args()

    processArgs(args, parser)





def processArgs(arguments, parser):
    args         = arguments.list
    name         = arguments.name
    hash         = arguments.hash
    recipient    = arguments.recipient
    amount       = arguments.amount
    leaseId      = arguments.leaseId
    network      = arguments.network
    type         = arguments.type
    stdin        = arguments.stdin.read().splitlines() if not sys.stdin.isatty() else []
    #stdin = ['3N6MFpSbbzTozDcfkTUT5zZ2sNbJKFyRtRj:700000000', '3NBC7ETcdPbf4QAXSop5UCJ53yX34aGPXoz:1000000']
    #stdin2 = ['3MyGpJh6Bb8auF3HtSr2dSJjqQVxgqLynpK:1000000000 3JxcLqcAKiUyvvLS8fk9SCS4taaCKUCqqLz:800000000']
    #stdinSeed = ['cool strike recall mother true topic road bright nature dilemma glide shift return mesh strategy']

    if name:
        name = name[0]

    if args[0] == 'accounts':
        Account.func(args, name, network, stdin)
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
        ConfigNew.setnode(args, network)
    elif args[0] == 'mass-transfer':
        MassTransfer.func(stdin)
    else:
        parser.error('Unrecognized input')


if __name__ == '__main__':
    main()