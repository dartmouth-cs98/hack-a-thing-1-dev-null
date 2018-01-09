from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
random_generator = Random.new().read

key = RSA.generate(1024, random_generator)
public_key = key.publickey()
# private_key = key.privatekey()
print("Your private key. Keep this safe. Anyone with your private key can make transactions on your behalf, aka steal all your KyleKoins.")

print(key.exportKey().decode())

print("Your public key / your address")
print(key.publickey().exportKey().decode())

# text = 'abcdefgh'
#
# hash = SHA256.new(text.encode()).digest()
#
# signature = key.sign(hash, '')
#
# text = 'abcdefgh'
#
# hash = SHA256.new(text.encode()).digest()
#
# print(public_key.verify(hash, signature))
