import configparser
import Account
import base58
import os

def writeToFile(fileName: str, account: Account):
    config = configparser.ConfigParser()
    config.read(fileName)
    secName = 'Account_{0}'.format(getAccountNumber(config.sections()))
    config.add_section(secName)
    config.set(secName, 'Address', account.address)
    config.set(secName, 'PublicKey', base58.b58encode(account.publicKey.__bytes__()))
    config.set(secName, 'PrivateKey', base58.b58encode(account.privateKey.__bytes__()))
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
    for sec in config.sections():
        if config.get(sec, 'address') == address:
            return sec
    raise Exception ("Option not found")


def getAccountNumber(secNameList):
    x = 0
    flag = True
    while flag:
        flag = False
        for name in secNameList:
            if str(x) in name:
                x += 1
                flag = True
    return x

'''config = configparser.ConfigParser()
config.read('config.ini')
secNameList = (config.sections())
print(secNameList)


print('3' in secNameList[4])
print(x)
'''