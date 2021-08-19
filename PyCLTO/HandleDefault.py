import configparser
from AccountFactory import AccountFactory
import bash

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
        config.read('Default.ini')
        return config.get('Default', 'seed')
    except:
        raise Exception('No account set as default')


def getDefaultAccount():
    return (AccountFactory(bash.CHAIN_ID).createFromSeed(getDefaultSeed()))

