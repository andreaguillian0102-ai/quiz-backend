from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DB_FILE = 'database.json'

# Function to load data from the file
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {}

# Function to save data to the file
def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/auth', methods=['POST'])
def handle_auth():
    db = load_db()
    data = request.json
    user = data.get('username')
    password = data.get('password')
    is_login = data.get('isLogin')

    if not is_login: # Registration
        if user in db:
            return jsonify({"success": False, "message": "User already exists"}), 400
        db[user] = {
            "password": password,
            "subjectCompletion": {},
            "quizScores": {}
        }
        save_db(db)
        return jsonify({"success": True, "message": "Registered successfully"})
    
    else: # Login
        if user in db and db[user]["password"] == password:
            return jsonify({
                "success": True, 
                "subjectCompletion": db[user].get("subjectCompletion", {}),
                "quizScores": db[user].get("quizScores", {})
            })
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/save', methods=['POST'])
def save_data():
    db = load_db()
    data = request.json
    user = data.get('username')
    if user in db:
        db[user]["subjectCompletion"] = data.get('subjectCompletion')
        db[user]["quizScores"] = data.get('quizScores')
        save_db(db)
        return jsonify({"success": True})
    return jsonify({"success": False}), 404

import os

if __name__ == '__main__':
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)