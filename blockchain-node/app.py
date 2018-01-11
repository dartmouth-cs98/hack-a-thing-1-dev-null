# app.py
# Blockchain API.
# Robin Jayaswal, Kyle Dotterrer
# Dartmouth CS98
# Winter, 2018

# Blockchain API implementation adapted from tutorial by Daniel van Flymen
# https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

import os
import json

from uuid import uuid4
from textwrap import dedent
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

from blockchain import Blockchain

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

node_identifier = str(uuid4()).replace('-', '')

# instantiate a new blockchain for this node
blockchain = Blockchain()

# ------------------------------------------------------------------------------
# API ROUTES

"""
Mine a new block.
"""
@app.route('/mine', methods=['GET'])
@cross_origin()
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message'       : 'New Block Forged',
        'index'         : block['index'],
        'transactions'  : block['transactions'],
        'proof'         : block['proof'],
        'previous_hash' : block['previous_hash'],
    }

    return jsonify(response), 200


"""
Add a new transaction to the blockchain.
"""
@app.route('/transactions/new', methods=['POST'])
@cross_origin()
def new_transaction():
    values = request.get_json()

    # sender should be public address, recipient and amount signed with private key
    unencrypted = json.loads(values["unencrypted"])
    signature = values["signature"]

    unencryptedToStr = json.dumps(unencrypted, sort_keys=True)

    key = RSA.importKey(format_public_key(unencrypted["sender"]))
    public_key = key.publickey()
    hash = SHA256.new(unencryptedToStr.encode()).digest()

    signatureValid = public_key.verify(hash, signature)
    if not signatureValid:
        return "Invalid Signature", 401


    required = ['sender', 'recipient', 'amount']
    if not all(k in unencrypted for k in required):
        return 'Missing unencrypted', 400

    index = blockchain.new_transaction(unencrypted['sender'], unencrypted['recipient'], unencrypted['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


"""
Get the current state of the entire blockchain.
"""
@app.route('/chain', methods=['GET'])
@cross_origin()
def chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


"""
List the network nodes known to this node.
"""
@app.route('/nodes/list', methods=['GET'])
@cross_origin()
def list_nodes():
    response = {
        'message': 'Known network nodes',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


"""
Register new nodes in the network.
"""
@app.route('/nodes/register', methods=['POST'])
@cross_origin()
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


"""
Resolve blockchain conflicts by finding consensus.
"""
@app.route('/nodes/resolve', methods=['GET'])
@cross_origin()
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message'   : 'Our chain was replaced',
            'new_chain' : blockchain.chain
        }
    else:
        response = {
            'message' : 'Our chain is authoritative',
            'chain'   : blockchain.chain
        }

    return jsonify(response), 200

# ------------------------------------------------------------------------------
# HELPERS

def format_public_key(key):
    if key[:10] == '-----BEGIN':
        return key
    else:
        return '-----BEGIN PUBLIC KEY-----\n' + key + '\n-----END PUBLIC KEY-----'

# ------------------------------------------------------------------------------
# SCRIPT

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port)
