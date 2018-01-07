import json
import hashlib

from time import time


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # genesis block
        self.new_block(previous_hash=1, proof=100)


    # create a new block and add it the chain
    def new_block(self, proof, previous_hash=None):

        block = {
            'index'         : len(self.chain) + 1,
            'timestamp'     : time(),
            'transactions'  : self.current_transactions,
            'proof'         : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []

        self.chain.append(block)
        return block


    # add a new transaction to the list of existing transactions
    # these transactions have yet to be mined into a block
    def new_transaction(self, sender, recipient, amount):

        self.current_transactions.append({
            'sender'    : sender,
            'recipient' : recipient,
            'amount'    : amount,
        })

        # return the index of the next block
        # (return the index of the block that this transaction will
        # be in at the point it is mined?)
        return self.last_block['index'] + 1


    def proof_of_work(self, prev_proof):

        proof = 0
        while not self.valid_proof(prev_proof, proof):
            proof += 1

        return proof


    @staticmethod
    def valid_proof(prev_proof, proof):
        guess = f'{prev_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'


    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    @property
    def last_block(self):
        return self.chain[-1]

if __name__ == '__main__':
    x = 5
    y = 0

    while hashlib.sha256(f'{x*y}'.encode()).hexdigest()[-1] != '0':
        y+=1

    print(y)
