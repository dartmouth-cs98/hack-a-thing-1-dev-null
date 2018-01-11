import requests
from base_url import BASE_URL

r = requests.get(BASE_URL + '/chain')
print(r.json())
