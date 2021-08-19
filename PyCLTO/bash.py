import argparse
from AccountFactory import AccountFactory
import sys
import configparser
import Config


def main():
    parser = argparse.ArgumentParser(description='LTO Network CLI client')
    parser.add_argument('list', type=str, nargs='+')
    #parser.add_argument('--name', type=str, nargs=1)


    args = parser.parse_args(['accounts', 'create', 'https://nodes.lto.network', 'so', 'io']).list
    #args = parser.parse_args()
    #print(args.list)
    #print(args.name)
    processArgs(args, parser)

    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))
    #print(parser.parse_args(['7', '-1', '42']))'''

    '''parser.add_argument('--x', type=float, default=1.0,
                        help='What is the first number?')
    parser.add_argument('--y', type=float, default=1.0,
                        help='What is the second number?')
    parser.add_argument('--operation', type=str, default='add',
                        help='What operation? Can choose add, sub, mul, or div')'''
    # args = processArgs(parser.parse_args(['test che ne so io']))

    # sys.stdout.write(str(calc(args)))
    # sys.stdout.write(str(args))
    # sys.stdout.write(str(args))

    '''for x in args:
        sys.stdout.write(x)
        sys.stdout.write(' ')'''

    # print(type(args))


def Account(args):
    factory = AccountFactory('L')
    if args[1] == 'create':
        account = factory.create()
        Config.writeToFile('config.ini', account)
    elif args[1] == 'list':
        print(Config.listAccounts('config.ini'))
    elif args[1] == 'remove':
        Config.removeAccount('config.ini', args[2])


def processArgs(args, parser):
    if args[0] == 'accounts':
        Account(args)
    elif args[0] == 'anchor':
        pass
    else:
        parser.error('Unrecognized input')



if __name__ == '__main__':
    main()
