import argparse
from AccountFactory import AccountFactory
from PyCLTO.Transactions import Transfer as Transf
from PyCLTO import PublicNode
import base58
import sys
import configparser
import Config
import HandleDefault as handle

CHAIN_ID = 'L'

def main():
    parser = argparse.ArgumentParser(description='LTO Network CLI client')
    parser.add_argument('list', type=str, nargs='+')
    parser.add_argument('--name', type=str, nargs=1)
    parser.add_argument('--hash', type=str, nargs=1)
    parser.add_argument('--recipient', type=str, nargs=1)
    parser.add_argument('--amount', type=str, nargs=1)


    #args = parser.parse_args(['accounts', 'create', 'divert manage prefer child kind maximum october hand manual connect fitness small symptom range sleep', '--name', 'foobar'])
    args = parser.parse_args(['transfer','--recipient', '3N8TQ1NLN8KcwJnVZM777GUCdUnEZWZ85Rb','--amount', '30000000'])
    #args = parser.parse_args(['accounts','set-default', 'ciccio'])
    print(args)
    processArgs(args, parser)


def Account(args, secName):
    factory = AccountFactory(CHAIN_ID)
    if args[1] == 'create':
        account = factory.create()
        Config.writeToFile('config.ini', account, secName)
    elif args[1] == 'list':
        print(Config.listAccounts('config.ini'))
    elif args[1] == 'remove':
        Config.removeAccount('config.ini', args[2])
    elif args[1] == 'set-default':
        Config.setDefault('config.ini', args[2])
    elif args[1] == 'seed':
        account = factory.createFromSeed(args[2])
        Config.writeToFile('config.ini', account, secName)

def Anchor(hash):
    if not hash:
        raise Exception ('No hash was passed')
    hash = hash[0]
    print(hash)

def Transfer(recipient, amount):
    if not recipient:
        raise Exception('Recipient field must be fulled')
    recipient = recipient[0]
    if not amount:
        raise Exception ('Amount field must be filled')
    amount = amount[0]
    '''defaultPubKey = Config.getDefaultPubKey()
    factory = AccountFactory('L')
    account = factory.createFromPublicKey(defaultPubKey)'''
    account = handle.getDefaultAccount()
    transfer = Transf.Transfer(recipient, int(amount))
    transfer.signWith(account)
    url = 'https://testnet.lto.network'
    node = PublicNode(url)
    node.broadcast(transfer)



def processArgs(arguments, parser):
    args      = arguments.list
    name      = arguments.name
    hash      = arguments.hash
    recipient = arguments.recipient
    amount    = arguments.amount

    if name:
        name = name[0]
        
    if args[0] == 'accounts':
        Account(args, name)
    elif args[0] == 'anchor':
        Anchor(hash)
    elif args[0] == 'transfer':
        Transfer(recipient, amount)
    else:
        parser.error('Unrecognized input')



if __name__ == '__main__':
    main()
