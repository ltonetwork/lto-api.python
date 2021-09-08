import configparser
from PyCLTO.AccountFactory import AccountFactory
import ConfigNew

def getSeedFromAddress(address):
    config = configparser.ConfigParser()
    config.read('L/accounts.ini')
    secName = ConfigNew.findAccountSection(address, config)
    if not secName:
        config.clear()
        config.read('T/accounts.ini')
        secName = ConfigNew.findAccountSection(address, config)
        if not secName:
            raise Exception ('No account found matching with default value')
        else:
            return config.get(secName, 'seed')
    else:
        return config.get(secName, 'seed')


def getAccount(address, config):
    if 'Node' in config.sections():
        chainId = config.get('Node', 'chainId')
    else:
        chainId = 'L'
    seed = getSeedFromAddress(address)
    account = AccountFactory(chainId).createFromSeed(seed)
    return account

def getDefaultPubKey():
    try:
        config = configparser.ConfigParser()
        config.read('default.ini')
        return config.get('Default', 'publickey')
    except:
        raise Exception('No account set as default')


def getDefaultAddress():
    try:
        config = configparser.ConfigParser()
        config.read('default.ini')
        return config.get('Default', 'address')
    except:
        raise Exception('No account set as default')


def getDefaultPrivKey():
    try:
        config = configparser.ConfigParser()
        config.read('default.ini')
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

