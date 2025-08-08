import pprint

import requests

"""
curl -X 'POST' \
  'http://5.63.153.31:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "string",
  "email": "string",
  "password": "string"
}'
"""
url = 'http://5.63.153.31:5051/v1/account/f755b9d2-4ae8-4f70-9b77-8f2b66339097'
headers = {'accept': 'text/plain'}

# json = {"login": "vmenshikov-test2",
#         "email": "vmenshikov-test2@mail.ru",
#         "password": "123456789"}

response = requests.put(url=url, headers=headers)
response_json = response.json()
print(response_json['resource']['rating']['quantity'])

pprint.pprint(response.status_code)
pprint.pprint(response.json())

