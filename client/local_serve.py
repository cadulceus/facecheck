import hashlib, pyperclip, random, requests, string
from manager import Vault
from flask import Flask, request, jsonify
from Tkinter import Tk

import numpy as np

app = Flask(__name__)
BACKEND_ADDR = "localhost:5005"
BACKEND = "http://{}".format(BACKEND_ADDR)
VALID_CHARS = ''.join(set(string.printable) - set(string.whitespace))

v = Vault()
j = jsonify

def gen_key(l=10, f="words.txt"):
    with open(f, 'r') as r:
        words = [w.strip() for w in r.readlines()]

    return ' '.join([random.choice(words).lower() for i in xrange(l)])

def gen_pass(l=16, c=VALID_CHARS):
    return ''.join([random.choice(c) for i in xrange(l)])

@app.route("/gen_pass")
def generate_password():
    global v
    return j({'status': 'success',
              'password': gen_pass()})

@app.route("/copy_pass")
def copy_password():
    global v
    if not request.args or 'service' not in request.args or not v.unlocked:
        return j({'status': 'bad args'})

    service = request.args['service'].lower()

    if service not in v.items:
        return j({'status': 'service not in vault'})
    password = v.items[service][0]['password']
    pyperclip.copy(password)
    return j({'status': 'success'})

@app.route("/train")
def train():
    global v
    v.collect_faces()
    v.train()
    print v.unlocked
    print v.pin
    print v.secret
    return j({'status': 'success'})

@app.route("/detect")
def detect():
    global v
    success = v.detect()
    return j({'status': 'success' if success else 'Facial recognition failed'})

@app.route("/edit_item", methods=["POST"])
def edit_item():
    global v
    if not request.json or 'service' not in request.json or 'id' not in request.json:
        return j({'status': 'error',
                  'message': 'entry id or service not provided'})

    if 'password' in request.json:
        password = request.json['password']
    else:
        password = gen_pass()

    success = v.edit_item(request.json['service'].lower(),
                          password)

    if not success:
        return j({'status': 'error'})

    return j({'status': 'success',
              'modified': success})
    

@app.route("/add_item", methods=["POST"])
def add_item():
    global v
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
    global v
    i = v.items
    i['status'] = 'success'
    return jsonify(i)

@app.route("/unlock")
def unlock():
    global v
    success = v.unlock()
    return j({'status': 'success' if success else 'error'})

@app.route("/lock")
def lock():
    global v
    v.lock()
    return j({'status': 'success'})

@app.route("/post_sync")
def post_sync():
    global v
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
    global v
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
    
@app.route("/import", methods=["POST"])
def vault_import():
    global v
    if not request.json or 'secret' not in request.json:
        return j({'status': 'error',
                  'message': 'missing pin argument'})
    
    secret = request.json['secret'].strip()

    h = hashlib.sha512()
    h.update(secret)
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
    global v
    if not request.args or 'pin' not in request.args:
        return j({'status': 'error',
                  'message': 'missing pin argument'})

    v.pin = request.args['pin'].strip()

    print v.pin
    print v.filename
    return j({'status': 'success'})

@app.route("/create")
def create():
    global v
    if not request.args or 'pin' not in request.args:
        return j({'status': 'error',
                  'message': 'missing pin argument'})
    v = Vault()
    v.pin = request.args['pin'].strip()
    secret = gen_key()
    v.secret = secret
    v.encrypted_secret = v.encrypt_secret(v.secret)
    v.unlocked = True
    v.encrypted_data = v.encrypt_items({})

    h = hashlib.sha512()
    h.update(v.secret)
    vault_id = h.hexdigest()

    resp = requests.post(BACKEND + '/sync', json={'id': vault_id, 'content': v._serialize().encode('base64')})

    return j({'status': 'success',
              'pin': v.pin,
              'sync': 'success' if resp.status_code == 200 else 'error',
              'secret': v.secret})

@app.route('/clear_training')
def clear_training():
    global v
    if not v.unlocked:
        return j({'status': 'error',
                  'message': 'vault must be unlocked to clear facial data'})

    v.training = {}
    v.images = []
    v.labels = np.array([])
    v.encrypted_training = ""

    if v.filename:
        try:
            v.save()
        except:
            return j({'status': 'error',
                      'message': 'could not open vault file'})

    return j({'status': 'success'})


@app.route("/save", methods=["POST"])
def save():
    global v
    if not request.json or 'filepath' not in request.json:
        return j({'status': 'error',
                  'message': 'missing filepath argument'})

    filename = request.json['filepath']
    v.filename = filename

    try:
        v.save()
    except:
        return j({'status': 'error',
                  'message': 'could not open vault file'})

    return j({'status': 'success'})


@app.route("/load", methods=["POST"])
def load():
    global v
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
