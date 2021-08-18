import argparse
from AccountFactory import AccountFactory
import sys
import configparser
import Config

def main():

    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))
    #print(parser.parse_args(['7', '-1', '42']))'''
    parser = argparse.ArgumentParser(description='LTO Network CLI client')
    parser.add_argument('list', type=str, nargs='+')

    '''parser.add_argument('--x', type=float, default=1.0,
                        help='What is the first number?')
    parser.add_argument('--y', type=float, default=1.0,
                        help='What is the second number?')
    parser.add_argument('--operation', type=str, default='add',
                        help='What operation? Can choose add, sub, mul, or div')'''
    #args = processArgs(parser.parse_args(['test che ne so io']))
    args = parser.parse_args(['accounts', 'create', 'ne', 'so', 'io']).list
    processArgs(args, parser)
    # sys.stdout.write(str(calc(args)))
    #sys.stdout.write(str(args))
    #sys.stdout.write(str(args))
    
    '''for x in args:
        sys.stdout.write(x)
        sys.stdout.write(' ')'''

    #print(type(args))

def Account(args):
    factory = AccountFactory('L')
    if args[1] == 'create':
        account = factory.create()
        #Config.getSec()
        Config.writeToFile('Pyclto/config.ini', account)
        '''print(account.address)
        print(account.publicKey)
        print(account.privateKey)'''
    print(args)

def processArgs(args, parser):
    if args[0] == 'accounts':
        Account(args)
    elif args[0] == 'anchor':
        pass
    else:
        parser.error('Unrecognized input')

def calc(args):
    if args.operation == 'add':
        return args.x + args.y
    elif args.operation == 'sub':
        return args.x - args.y
    elif args.operation == 'mul':
        return args.x * args.y
    elif args.operation == 'div':
        return args.x / args.y


if __name__ == '__main__':
    main()