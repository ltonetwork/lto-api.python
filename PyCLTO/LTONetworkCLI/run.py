import argparse
parser = argparse.ArgumentParser()
parser.add_argument('args', nargs=argparse.REMAINDER)
args = parser.parse_args().args
print (args)