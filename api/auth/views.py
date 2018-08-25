from flask import Flask, jsonify, request
from api.database import Database
from api import app


db = Database()

@app.route('/api/v1/auth/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    if db.get_by_argument('users','email', email):
        return jsonify({'message': 'user already exists'}), 409
    db.insert_user_data(username, email, password)
    return jsonify({'message':'Account created successfully'}), 201
