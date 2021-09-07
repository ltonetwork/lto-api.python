def Account(args, secName):
    factory = AccountFactory(CHAIN_ID)
    if args[1] == 'create':
        account = factory.create()
        ConfigNew.writeToFile('config.ini', account, secName)
    elif args[1] == 'list':
        print(ConfigNew.listAccounts('config.ini'))
    elif args[1] == 'remove':
        ConfigNew.removeAccount('config.ini', args[2])
    elif args[1] == 'set-default':
        ConfigNew.setDefault('config.ini', args[2])
    elif args[1] == 'seed':
        account = factory.createFromSeed(args[2])
        ConfigNew.writeToFile('config.ini', account, secName)
