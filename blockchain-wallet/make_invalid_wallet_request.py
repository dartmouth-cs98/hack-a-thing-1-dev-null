from wallet import send_money
from generate_wallet import create_wallet

privatekey, publickey = create_wallet()

badPrivateKey, badPublicKey = create_wallet()

response = send_money("robin", 100, privatekey=badPrivateKey, publickey=publickey)

print(response)
assert(response == 401)
