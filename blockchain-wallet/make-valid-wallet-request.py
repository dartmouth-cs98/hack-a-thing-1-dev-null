from wallet import send_money
from generate_wallet import create_wallet

privatekey, publickey = create_wallet()

response = send_money("robin", 100, privatekey=privatekey, publickey=publickey)

assert(response == 201)
