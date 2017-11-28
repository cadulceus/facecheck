import hashlib, random, requests, string
from manager import Vault
from flask import Flask, request, jsonify

app = Flask(__name__)
BACKEND_ADDR = "localhost:5005"
BACKEND = "http://{}".format(BACKEND_ADDR)
VALID_CHARS = ''.join(set(string.printable) - set(string.whitespace))

v = Vault()
j = jsonify

def gen_pass(l=16, c=VALID_CHARS):
    return ''.join([random.choice(c) for i in xrange(l)])

@app.route("/edit_item", methods=["POST"])
def edit_item():
    if not request.json or 'service' not in request.json or 'id' not in request.json:
        return j({'status': 'error',
                  'message': 'entry id or service not provided'})

    if 'password' in request.json:
        password = request.json['password']
    else:
        password = gen_pass()

    success = v.edit_item(request.json['service'].lower(),
                          request.json['id'].lower(),
                          password)

    if not success:
        return j({'status': 'error'})

    return j({'status': 'success',
              'modified': success})
    

@app.route("/add_item", methods=["POST"])
def add_item():
    if not request.json or 'username' not in request.json or 'service' not in request.json:
        return j({'status': 'error',
                  'message': 'username or service not provided'})

    if 'password' in request.json:
        password = request.json['password']
    else:
        password = gen_pass()

    if 'entry_name' in request.json:
        entry_name = request.json['entry_name']
    else:
        entry_name = request.json['service']

    success = v.add_item(request.json['service'].lower(), entry_name, request.json['username'], password)
    if not success:
        return j({'status': 'error'})

    return j({'status': 'success',
              'added': success})
    

@app.route("/items")
def items():
    i = v.items
    i['status'] = 'success'
    return jsonify(i)

@app.route("/unlock")
def unlock():
    success = v.unlock()
    return j({'status': 'success' if success else 'error'})

@app.route("/lock")
def lock():
    v.lock()
    return j({'status': 'success'})

@app.route("/post_sync")
def post_sync():
    if not v.secret:
        return j({'status': 'error',
                  'message': 'vault must have been unlocked to upload the most recent sync'})

    h = hashlib.sha512()
    h.update(v.secret)
    vault_id = h.hexdigest()

    resp = requests.post(BACKEND + '/sync', json={'id': vault_id, 'content': v._serialize().encode('base64')})
    if resp.status_code != 200:
        return j({'status': 'error',
                  'message': 'error contacting sync server'})
    return j({'status': 'success'})

@app.route("/get_sync")
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

    success = v._deserialize(data['content'].decode('base64'))
    if not success:
        return j({'status': 'error',
                  'message': 'error deserializing vault contents'})

    if v.filename:
        with open(v.filename, 'w') as w:
            w.write(data['content'].decode('base64'))

    return j({'status': 'success'})
    

@app.route("/set_pin")
def set_pin():
    if not request.args or 'pin' not in request.args:
        return j({'status': 'error',
                  'message': 'missing pin argument'})

    v.pin = request.args['pin'].strip()

    print v.pin
    print v.filename
    return j({'status': 'success'})

@app.route("/load", methods=["POST"])
def load():
    if not request.json or 'filepath' not in request.json:
        return j({'status': 'error',
                  'message': 'missing filepath argument'})

    v.filename = request.json['filepath']
    try:
        v.load()
    except:
        return j({'status': 'error',
                  'message': 'could not open vault file'})

    return j({'status': 'success'})

@app.route("/")
def index():
    return "Hello World!"
