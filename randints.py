#!/usr/bin/env python

import random

def main(args):
    lo = int(args[0])
    hi = int(args[1])
    howmany = int(args[2])
    for i in range(howmany):
        print(random.randint(lo, hi))

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])

