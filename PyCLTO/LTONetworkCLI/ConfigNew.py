import configparser
from PyCLTO.Account import Account
import base58
from nacl.signing import SigningKey, VerifyKey
import os

CHAIN_ID = 'L'

def writeToFile(path, account, secName):
    error = 'Name'
    if not secName:
        secName = account.address
        error = 'Address'
    config = configparser.ConfigParser()
    if os.path.exists(path):
        config.read(path)
        if not nameAlreadyPresent(secName):
            config.add_section(secName)
            config.set(secName, 'Address', account.address)
            config.set(secName, 'PublicKey', base58.b58encode(account.publicKey.__bytes__()))
            config.set(secName, 'PrivateKey', base58.b58encode(account.privateKey.__bytes__()))
            config.set(secName, 'Seed', account.seed)
            config.write(open(path, 'w'))
        else:
            raise Exception('{} already present'.format(error))
    else:
        config.add_section(secName)
        config.set(secName, 'Address', account.address)
        config.set(secName, 'PublicKey', base58.b58encode(account.publicKey.__bytes__()))
        config.set(secName, 'PrivateKey', base58.b58encode(account.privateKey.__bytes__()))
        config.set(secName, 'Seed', account.seed)
        config.write(open(path, 'w'))

    config.clear()
    if not os.path.exists('L/config.ini'):
        setDefaultAccount(secName, account.address)
    else:
        config.read('L/config.ini')
        if 'Default' not in config.sections():
            setDefaultAccount(secName, account.address)

def nameAlreadyPresent(name):
    config = configparser.ConfigParser()
    config.read('L/accounts.ini')
    config.read('T/accounts.ini')
    if name in config.sections():
        return True
    return False

def getAddressFromName(name):
    config = configparser.ConfigParser()
    config.read('L/accounts.ini')
    if name not in config.sections():
        config.read('T/accounts.ini')
        if name not in config.sections():
            raise Exception('Account need to be created first')
        else:
            address = config.get(name, 'address')
            chainId = 'T'
    else:
        address = config.get(name, 'address')
        chainId = 'L'
    return address, chainId

def setDefaultAccount(name, address = ''):
    if not address:
        address, chainId = getAddressFromName(name)
    config = configparser.ConfigParser()
    if os.path.exists('L/config.ini'):
        config.read('L/config.ini')
        if 'Node' in config.sections():
            savedChainId = config.get('Node', 'chainid')
            if savedChainId and savedChainId != chainId:
                print('Attention!, Account belongs to a different network than the stored one')
        if 'Default' not in config.sections():
            config.add_section('Default')
            config.set('Default', 'account', address)
        else:
            config.set('Default', 'account', address)

    else:
        config.add_section('Default')
        config.set('Default', 'account', address)
    config.write(open('L/config.ini', 'w'))



def listAccounts():
    config = configparser.ConfigParser()
    config.read('L/accounts.ini')
    listL = config.sections()
    config.clear()
    config.read('T/accounts.ini')
    listT = config.sections()
    return listL, listT

def getNewDefault():
    config = configparser.ConfigParser()
    config.read('L/accounts.ini')
    if os.path.exists('L/accounts.ini') and config.sections() != []:
        sections = config.sections()
        address = config.get(sections[0], 'address')
        setDefaultAccount(name='placeholder', address=address)
    else:
        config.clear()
        config.read('T/accounts.ini')
        if os.path.exists('L/accounts.ini') and config.sections() != []:
            sections = config.sections()
            address = config.get(sections[0], 'address')
            setDefaultAccount(name='placeholder', address=address)


def removeDefault(address):
    config = configparser.ConfigParser()
    config.read('L/config.ini')
    if 'Default' in config.sections():
        if config.get('Default', 'account') == address:
            config.remove_section('Default')
            config.write(open('L/config.ini', 'w'))
            # getNewDefault()

def removeAccount(name):

    # check into the L directory
    config = configparser.ConfigParser()
    config.read('L/accounts.ini')
    if not name in config.sections():
        # in case the name provided is an address of an account registered under a name
        secName = findAccountSection(name, config)
        if secName in config.sections():
            address = config.get(secName, 'address')
            config.remove_section(secName)
            config.write(open('L/accounts.ini', 'w'))
            removeDefault(address)
        else:
            # check into the T directory
            config.clear()
            config.read('T/accounts.ini')
            if not name in config.sections():
                secName = findAccountSection(name, config)
                if secName in config.sections():
                    address = config.get(secName, 'address')
                    config.remove_section(secName)
                    config.write(open('T/accounts.ini', 'w'))
                    removeDefault(address)
                else:
                    raise Exception('Account does not exist')
            else:
                address = config.get(name, 'address')
                config.remove_section(name)
                config.write(open('T/accounts.ini', 'w'))
                removeDefault(address)
    else:
        address = config.get(name, 'address')
        config.remove_section(name)
        config.write(open('L/accounts.ini', 'w'))
        removeDefault(address)


# it returns the account section name from the address provided
def findAccountSection(address, config):
    for sec in config.sections():
        if config.get(sec, 'address') == address:
            return sec
    return ''




def setnode(args, network):
    if len(args) == 2:
        node = args[1]
    else :
        raise Exception('1 Node Parameter Required')

    if network:
        network = network[0]
        if network not in ['T', 'L']:
            raise Exception('Wrong chain ID')
    else:
        network = CHAIN_ID

    config = configparser.ConfigParser()
    if os.path.exists('L/config.ini'):
        config.read('L/config.ini')
        if 'Node' not in config.sections():
            config.add_section('Node')
            config.set('Node', 'ChainId', network)
            config.set('Node', 'URL', node)
        else:
            config.set('Node', 'ChainId', network)
            config.set('Node', 'URL', node)
    else:
        config.add_section('Node')
        config.set('Node', 'ChainId', network)
        config.set('Node', 'URL', node)
    config.write(open('L/config.ini', 'w'))


