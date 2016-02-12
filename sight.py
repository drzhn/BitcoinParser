#!/usr/bin/python
from blocktools import *
from block import Block, BlockHeader
from postgres import PgHash
from os import listdir


def parse(blockchain, pg):
    counter = 0
    while True:
        print "Block #"+str(counter), "| transactions in database:", pg.index
        try:
            block = Block(blockchain, pg)
        except struct.error:
            break
        else:
            # block.toString()
            pass
        counter += 1


def main():
    # if len(sys.argv) < 2:
    #     print 'Usage: sight.py filename'
    # else:
    #     with open(sys.argv[1], 'rb') as blockchain:
    #         parse(blockchain)
    dir = 'blocks'
    pg = PgHash()
    pg.refresh_db()
    for filename in listdir(dir):
        with open(dir + "/" + filename, 'rb') as blockchain:
            print "=========== FILE: " + filename + " ============="
            parse(blockchain, pg)


if __name__ == '__main__':
    main()
