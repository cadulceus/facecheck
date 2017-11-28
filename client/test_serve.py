import requests

ENDPOINT = 'http://localhost:5000'
resp = requests.post(ENDPOINT + '/load', json={'filepath': 'test.fcvault'})
print resp.json()

resp = requests.get(ENDPOINT + '/set_pin?pin=1234')
print resp.json()

resp = requests.get(ENDPOINT + '/unlock')
print resp.json()

resp = requests.get(ENDPOINT + '/items')
print resp.json()

resp = requests.post(ENDPOINT + '/add_item', json={'service': 'google.com',
                                                   'entry_name': 'Personal Email',
                                                   'username': 'test@gmail.com'})
print resp.json()
x = resp.json()

resp = requests.get(ENDPOINT + '/items')
print resp.json()

resp = requests.get(ENDPOINT + '/post_sync')
print resp.json()

resp = requests.get(ENDPOINT + '/get_sync')
print resp.json()

resp = requests.get(ENDPOINT + '/items')
print resp.json()

resp = requests.post(ENDPOINT + '/edit_item', json={'service': 'google.com',
                                                   'id': x['added']['id'],
                                                   'password': 'modified_password'})
print resp.json()

resp = requests.get(ENDPOINT + '/post_sync')
print resp.json()

resp = requests.get(ENDPOINT + '/get_sync')
print resp.json()

resp = requests.get(ENDPOINT + '/items')
print resp.json()

resp = requests.get(ENDPOINT + '/copy_pass?service=google.com')
print resp.json()

resp = requests.get(ENDPOINT + '/lock')
print resp.json()

resp = requests.get(ENDPOINT + '/items')
print resp.json()
