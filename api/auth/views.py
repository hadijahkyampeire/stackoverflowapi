import jwt
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from api.database import Database
from api.models import User
from api import app


db = Database()

@app.route('/api/v1/auth/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])
    if db.get_by_argument('users','email', email):
        return jsonify({'message': 'user already exists'}), 409
    db.insert_user_data(username, email, password)
    return jsonify({'message':'Account created successfully'}), 201

@app.route('/api/v1/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data['email']
    password = data['password']
    db_query = db.get_by_argument('users','email', email)
    user = User(db_query[0], db_query[1], db_query[2], db_query[3])
    print(user)
    if user.email == data['email'] and check_password_hash(user.password, data['password']):
        #Generate token
        token = jwt.encode(
                        {'email': user.email,
                         'exp': datetime.utcnow() +
                         timedelta(days=10, minutes=60)
                         }, 'mysecret')
        if token:
            response = {
                'message': 'You logged in successfully.',
                'token': token.decode('UTF-8'),
                'email': user.email,
                'username': user.username,
                'Id': user.id
            }
        return make_response(jsonify(response)), 200
    return jsonify({'message':'Invalid username or password, try again or create an account'}), 401
    

