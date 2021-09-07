import configparser
from PyCLTO.AccountFactory import AccountFactory


def getDefaultPubKey():
    try:
        config = configparser.ConfigParser()
        config.read('Default.ini')
        return config.get('Default', 'publickey')
    except:
        raise Exception('No account set as default')


def getDefaultAddress():
    try:
        config = configparser.ConfigParser()
        config.read('Default.ini')
        return config.get('Default', 'address')
    except:
        raise Exception('No account set as default')


def getDefaultPrivKey():
    try:
        config = configparser.ConfigParser()
        config.read('Default.ini')
        return config.get('Default', 'privatekey')
    except:
        raise Exception('No account set as default')


def getDefaultSeed():
    try:
        config = configparser.ConfigParser()
        config.read('default.ini')
        return config.get('Default', 'seed')
    except:
        raise Exception('No account set as default')


def getDefaultAccount(CHAIN_ID):
    return (AccountFactory(CHAIN_ID).createFromSeed(getDefaultSeed()))

