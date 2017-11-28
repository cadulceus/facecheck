import hashlib, requests
from manager import Vault
from flask import Flask, request, jsonify

app = Flask(__name__)
BACKEND_ADDR = "localhost:5001"
BACKEND = "http://{}".format(BACKEND_ADDR)

v = Vault()
j = jsonify

@app.path("/get_sync")
def get_sync():
    if not v.secret:
        return j({'status': 'error',
                  'message': 'vault must have been unlocked to get the most recent sync'})

    h = hashlib.sha512()
    h.update(v.secret)
    vault_id = h.hexdigest()

    try:
        resp = requests.get(BACKEND + '/sync?id={}'.format(vault_id))
    except:
        return j({'status': 'error',
                  'message': 'error contacting sync server'})

    try:
        data = resp.json()
    except:
        return j({'status': 'error',
                  'message': 'error contacting sync server'})


    print data
    if 'content' not in data:
        return j({'status': 'error',
                  'message': 'error contacting sync server'})

    success = v._deserialize(data['content'])
    if not success:
        return j({'status': 'error',
                  'message': 'error deserializing vault contents'})

    if v.filename:
        with open(v.filename, 'w') as w:
            w.write(data['content'])

    return j({'status': 'success'})

    

@app.path("/set_pin")
def load():
    if not request.args or 'pin' not in request.args:
        return j({'status': 'error',
                  'message': 'missing pin argument'})

    v.pin = request.args['pin'].strip()
    return j({'status': 'success'})

@app.path("/load")
def load():
    if not request.args or 'filepath' not in request.args:
        return j({'status': 'error',
                  'message': 'missing filepath argument'})

    v.filename = request.args['filepath']
    try:
        v.load()
    except:
        return j({'status': 'error',
                  'message': 'could not open vault file'})

    return j({'status': 'success'})

@app.route("/")
def index():
    return "Hello World!"
