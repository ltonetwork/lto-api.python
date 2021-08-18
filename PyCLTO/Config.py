import configparser
import Account
import base58
import os

def writeToFile(fileName: str, account: Account):
    config = configparser.ConfigParser()
    config.read(fileName)
    config.add_section('Account')
    config.set('Account', 'Address', account.address)
    config.set('Account', 'PublicKey', base58.b58encode(account.publicKey.__bytes__()))
    config.set('Account', 'PrivateKey', base58.b58encode(account.privateKey.__bytes__()))
    config.write(open(fileName, 'w'))

def listAccounts(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return (config.sections())

def removeAccount(filename, address):
    config = configparser.ConfigParser()
    config.read(filename)
    config.remove_section(findAccountSection(address, config))
    config.write(open(filename, 'w'))


# it returns the account section name from the addresses provided
def findAccountSection(address, config):
    
    '''print(config.get('testing', 'addr'))
    need to add a control in case there is not the option'''
    for sec in config.sections():
        if config.get(sec, 'address') == address:
            return sec
    raise Exception ("Option not found")

'''config = configparser.ConfigParser()
config.read('config.ini')
print(findAccountSection('22', config))'''

