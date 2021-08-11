import base58
from PyCLTO import AccountFactory
from nacl.signing import VerifyKey
from PyCLTO.PublicNode import PublicNode

def displayAccount(account):
    if account.privateKey:
        print("The account has been created \nPublicKey: {}\nPrivateKe: y{}\nAddress: {}"
          .format(base58.b58encode(account.publicKey.__bytes__()),
                  base58.b58encode(account.privateKey.__bytes__()), account.address))
    else:
        print("The account has been created \nPublicKey: y{}\nAddress: {}"
              .format(base58.b58encode(account.publicKey.__bytes__()), account.address))

def getInput(prompt, start, end):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Wrong input, type again.")
            continue

        if value not in range(start, end+1):
            print("Sorry, value not in range, type again.")
            continue
        else:
            break
    return value

def Program():
    factory = AccountFactory.AccountFactory('L')
    url = 'https://testnet.lto.network'
    publicNode = PublicNode(url)

    print("User guide:")
    x = getInput("Press 0 to create an account \nPress 1 to get a balance from an address\nPress 2 to terminate the process\n", 0, 2)

    if x == 0:
        y = getInput("Press 0 to create a NEW account \nPress 1 to retrieve an account from own informations\n", 0, 1)
        if y == 0:
            account = factory.create()
            displayAccount(account)
        elif y == 1:
            z = getInput("You have selected create an account from inserted data:\nPress 0 to enter the Public Key\nPress 1 to enter the Private Key\nPress 2 to enter the seed\n", 0, 2)
            if z == 0:
                pubKey = input("Enter the Public Key\n")
                account = factory.createFromPublicKey(VerifyKey(base58.b58decode(pubKey)))
                displayAccount(account)
            elif z == 1:
                privKey = base58.b58decode(input("Enter the Private Key\n"))
                account = factory.createFromPrivateKey(VerifyKey(base58.b58decode(privKey)))
                displayAccount(account)
            elif z == 2:
                seed = input("Enter the seed\n")
                account = factory.createFromSeed(seed)
                displayAccount(account)

            else:
                print()
    elif x == 1:
        address = input("Enter the address\n")
        #address = '3N5PoiMisnbNPseVXcCa5WDRLLHkj7dz4Du'
        print(PublicNode.balance(address))
        #print("Balance: ", value['balance'] / 100000000)
        #print(value)
Program()
