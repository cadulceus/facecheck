import db, hashlib
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/sync", methods=["GET", "POST"])
def sync():
    if request.method == "POST":
        if not request.json:
            return jsonify({'status': 'error'})

        data = request.json
        if 'id' not in data or 'content' not in data:
            return jsonify({'status': 'error'})

        db.update_vault(data['id'], data['content'])
        return jsonify({'status': 'success'})

    else:
        if not request.args or 'id' not in request.args:
            return jsonify({'status': 'error'})
        
        _id = request.args['id']
        vault = db.get_vault(_id)
        if not vault:
            return jsonify({'status': 'error'})

        return jsonify({'status': 'success',
                        'content': vault.content})

@app.route("/")
def index():
    return "Hello World!"

