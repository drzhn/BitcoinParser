from blocktools import *
import hashlib
from postgres import PgHash

class BlockHeader:
    def __init__(self, blockchain):
        self.version = uint4(blockchain)
        self.previousHash = hash32(blockchain)
        self.merkleHash = hash32(blockchain)
        self.time = uint4(blockchain)
        self.bits = uint4(blockchain)
        self.nonce = uint4(blockchain)

    def toString(self):
        print "Version:\t %d" % self.version
        print "Previous Hash\t %s" % hashStr(self.previousHash)
        print "Merkle Root\t %s" % hashStr(self.merkleHash)
        print "Time\t\t %s" % str(self.time)
        print "Difficulty\t %8x" % self.bits
        print "Nonce\t\t %s" % self.nonce


class Block:
    def __init__(self, blockchain, pg):
        self.magicNum = uint4(blockchain)
        self.blocksize = uint4(blockchain)
        self.setHeader(blockchain)
        self.txCount = varint(blockchain)
        self.Txs = []

        for i in range(0, self.txCount):
            tx = Tx(blockchain, pg)
            self.Txs.append(tx)

    def setHeader(self, blockchain):
        self.blockHeader = BlockHeader(blockchain)

    def toString(self):
        print ""
        print "Magic No: \t%8x" % self.magicNum
        print "Blocksize: \t", self.blocksize
        print ""
        print "#" * 10 + " Block Header " + "#" * 10
        self.blockHeader.toString()
        print
        print "##### Tx Count: %d" % self.txCount
        for t in self.Txs:
            t.toString()


class Tx:
    def __init__(self, blockchain, pg):
        self.version = uint4(blockchain)
        self.inCount = varint(blockchain)
        self.inputs = []

        transactionVersionNumber = self.version
        inputCount = self.inCount
        transactionBin = struct.pack('I', transactionVersionNumber) + packWithVarint(inputCount)
        hashlist = []
        for i in range(0, self.inCount):
            input = txInput(blockchain)
            self.inputs.append(input)

            transactionHash = input.prevhash  # hash32(blockchain)
            hashlist.append(str(hashStr(transactionHash)))

            transactionIndex = input.txOutId  # uint32_t(blockchain)
            scriptLength = input.scriptLen  # varint(blockchain)
            inputScript = input.scriptSig  # script(blockchain, scriptLength)
            sequenceNumber = input.seqNo  # uint32_t(blockchain)
            transactionBin = transactionBin + transactionHash[::-1] + struct.pack('I',
                                                                                  transactionIndex) + packWithVarint(
                scriptLength) + inputScript + struct.pack('I', sequenceNumber)
        self.outCount = varint(blockchain)
        self.outputs = []

        outputCount = self.outCount
        transactionBin = transactionBin + packWithVarint(outputCount)
        if self.outCount > 0:
            for i in range(0, self.outCount):
                output = txOutput(blockchain)
                self.outputs.append(output)

                value = output.value  # uint64_t(f)
                outputScriptLength = output.scriptLen  # (f)
                outputScript = output.pubkey  # script(f, outputScriptLength)
                transactionBin = transactionBin + struct.pack('Q', value) + packWithVarint(
                    outputScriptLength) + outputScript
        self.lockTime = uint4(blockchain)
        self.transactionLockTime = self.lockTime
        transactionBin = transactionBin + struct.pack('I', self.transactionLockTime)
        self.transactionHash = hashlib.sha256(hashlib.sha256(transactionBin).digest()).digest()[::-1]
        pg.insert_hash(self.transactionHash.encode('hex_codec'))
        # print self.transactionHash.encode('hex_codec')
        # print hashlist
        pg.insert_previous(self.transactionHash.encode('hex_codec'), hashlist)

    def toString(self):
        print ""
        print "=" * 10 + " New Transaction " + "=" * 10
        print "Tx Version:\t %d" % self.version
        print "Inputs:\t\t %d" % self.inCount
        for i in self.inputs:
            i.toString()

        print "Outputs:\t %d" % self.outCount
        for o in self.outputs:
            o.toString()
        print "Lock Time:\t %d" % self.lockTime
        print "TransactionLockTime:\t %d" % self.transactionLockTime
        print "TransactionHash:\t", self.transactionHash.encode('hex_codec')


class txInput:
    def __init__(self, blockchain):
        self.prevhash = hash32(blockchain)
        self.txOutId = uint4(blockchain)
        self.scriptLen = varint(blockchain)
        self.scriptSig = blockchain.read(self.scriptLen)
        self.seqNo = uint4(blockchain)

    def toString(self):
        print "Previous Hash:\t %s" % hashStr(self.prevhash)
        print "Tx Out Index:\t %8x" % self.txOutId
        print "Script Length:\t %d" % self.scriptLen
        print "Script Sig:\t %s" % hashStr(self.scriptSig)
        print "Sequence:\t %8x" % self.seqNo


class txOutput:
    def __init__(self, blockchain):
        self.value = uint8(blockchain)
        self.scriptLen = varint(blockchain)
        self.pubkey = blockchain.read(self.scriptLen)

    def toString(self):
        print "Value:\t\t %d" % self.value
        print "Script Len:\t %d" % self.scriptLen
        print "Pubkey:\t\t %s" % hashStr(self.pubkey)
