import requests

ENDPOINT = 'http://localhost:5000'
resp = requests.post(ENDPOINT + '/load', json={'filepath': 'test.fcvault'})
print resp.content

resp = requests.get(ENDPOINT + '/set_pin?pin=1234')
print resp.content

resp = requests.get(ENDPOINT + '/unlock')
print resp.content

resp = requests.get(ENDPOINT + '/post_sync')
print resp.content

resp = requests.get(ENDPOINT + '/get_sync')
print resp.content

resp = requests.get(ENDPOINT + '/lock')
print resp.content
