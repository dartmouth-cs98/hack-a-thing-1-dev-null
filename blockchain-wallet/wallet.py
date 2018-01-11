# wallet.py
# Robin Jaywaswal, Kyle Dotterrer
# Dartmouth CS98
# Winter, 2018

import os
import json
import requests
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

PRIVATE_KEY = os.environ['COIN_PRIVATE']
PUBLIC_KEY =  os.environ['COIN_PUBLIC']
PREFERRED_NODE = 'http://localhost:5000'

def send_money(reciever, amount, privatekey=PRIVATE_KEY, publickey=PUBLIC_KEY):
    body = json.dumps({
        u"sender": publickey,
        u"recipient": reciever,
        u"amount": amount,
    }, sort_keys=True)

    hash = SHA256.new(body.encode()).digest()

    key = RSA.importKey(privatekey)
    signature = key.sign(hash, '')

    r = requests.post(PREFERRED_NODE + '/transactions/new', json={"unencrypted": body, "signature": signature})
    return r.status_code

send_money("kylesaddress", 100)
