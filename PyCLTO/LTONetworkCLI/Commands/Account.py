from PyCLTO.AccountFactory import AccountFactory
from PyCLTO.LTONetworkCLI import ConfigNew


def func(args, secName, network):
    if not network:
        CHAIN_ID = 'L'
    else:
        CHAIN_ID = network[0]

    factory = AccountFactory(CHAIN_ID)

    if args[1] == 'create':
        account = factory.create()
        ConfigNew.writeToFile('{}/accounts.ini'.format(CHAIN_ID), account, secName)

    elif args[1] == 'list':
        print(ConfigNew.listAccounts())
    elif args[1] == 'remove':
        ConfigNew.removeAccount(args[2])
    elif args[1] == 'set-default':
        ConfigNew.setDefaultAccount(args[2])
    elif args[1] == 'seed':
        account = factory.createFromSeed(args[2])
        ConfigNew.writeToFile('{}/accounts.ini'.format(CHAIN_ID), account, secName)
