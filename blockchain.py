# blockchain.py
# Blockchain class definition / implementation.
# Robin Jayaswal, Kyle Dotterrer
# Dartmouth CS98
# Winter 2018

# Blockchain class implementation adapted from tutorial by Daniel van Flymen
# https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

import json
import hashlib
import requests

from time import time
from urllib.parse import urlparse


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        # genesis block
        self.new_block(previous_hash=1, proof=100)


    @property
    def last_block(self):
        return self.chain[-1]


    """
    Create a new block and add it the chain.
    Arguments
        proof (int): the proof of work attached to this block
        previous_hash (string): the hash of the previous block
    Return
        (dictionary) the newly mined block
    """
    def new_block(self, proof, previous_hash=None):
        block = {
            'index'         : len(self.chain) + 1,
            'timestamp'     : time(),
            'transactions'  : self.current_transactions,
            'proof'         : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1]),
        }

        # all current transactions are added to the most recently mined block,
        # therefore, the list of current (pending) transactions that have not
        # yet been attached to a block is reset
        self.current_transactions = []

        self.chain.append(block)
        return block


    """
    Add a new transaction to the list of existing transactions -
    these transactions have yet to be mined into a block.

    Arguments
        sender (string): identifer for the transaction sender
        recipient (string): identifer for the transaction recipient
        amount (int): value of the transaction
    Return
        (int): the index of the block that this transaction will be added to
    """

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


    """
    Compute a proof of work, conditional on the previous proof.
    Arguments
        prev_proof (int): the proof of work for the previous block
    Return
        (int): the computed proof of work
    """
    def proof_of_work(self, prev_proof):
        proof = 0
        while not self.valid_proof(prev_proof, proof):
            proof += 1

        return proof


    """
    Determine if the given chain is valid.
    Arguments
        chain (list): the chain under investigation
    Return
        (boolean): True if the given chain is valid, False otherwise
    """
    def valid_chain(self, chain):
        # begin inspection at the genesis block of the chain
        prev_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            # the hash of the previous block must match the value stored
            # in the current block
            if block['previous_hash'] != self.hash(prev_block):
                return False

            # the proof of work for the current block must be valid,
            # conditional on the proof attached to the previous block
            if not self.valid_proof(prev_block['proof'], block['proof']):
                return False

            prev_block = block
            current_index += 1

        return True


    """
    Register a new node in the blockchain network.
    Arguments
        address (string): the address of the node to add
    Return
        None
    """
    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)


    """
    Ensure the consensus is maintained by this node.
    Arguments
        None
    Return
        (boolean): True if this node's chain has been replaced, False otherwise
    """
    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True

        return False


    """
    Determine if the given proof of work is valid.
    Arguments
        prev_proof (int): the proof of work attached to the previous block
        proof (int): the candidate proof of work
    Return
        (boolean): True if the given candidate proof is valid, False otherwise
    """
    @staticmethod
    def valid_proof(prev_proof, proof):
        guess = f'{prev_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'


    """
    Hash a block.
    Arguments
        block (dictionary): the block to hash
    Return
        (string): the resulting hex digest string
    """
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


if __name__ == '__main__':
    print('Hello, Blockchain!')
