import os
import requests

PRIVATE_KEY = os.environ['KYLEKOIN_PRIVATE']
PUBLIC_KEY = os.environ['KYLEKOIN_PUBLIC']
PREFERRED_NODE = 'none'

def send_money(reciever, amount):
    body = json.dumps({u"sender": u"Sounds great! I'll get right on it!"})
