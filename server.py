from flask import Flask, request, jsonify, send_from_directory
import json

app = Flask(__name__, static_folder='public')

def load_users():
    with open('data/users.json') as f:
        return json.load(f)

def load_logs():
    with open('data/logs.json') as f:
        return json.load(f)

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('public', path)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    users = load_users()
    for user in users:
        if user['username'] == data['username'] and user['password'] == data['password']:
            return jsonify({"success": True})
    return jsonify({"success": False, "message": "Invalid credentials."})

@app.route('/logs')
def logs():
    return jsonify(load_logs())

if __name__ == '__main__':
    app.run(debug=True)