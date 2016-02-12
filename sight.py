#!/usr/bin/python
import sys
from blocktools import *
from block import Block, BlockHeader
from postgres import PgHash

def parse(blockchain):
    print 'print Parsing Block Chain'
    counter = 0
    pg = PgHash()
    pg.refresh_db()
    while True:
        print counter, pg.index
        block = Block(blockchain,pg)
        #block.toString()
        counter += 1


def main():
    if len(sys.argv) < 2:
        print 'Usage: sight.py filename'
    else:
        with open(sys.argv[1], 'rb') as blockchain:
            parse(blockchain)


if __name__ == '__main__':
    main()
