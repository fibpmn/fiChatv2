from app import app
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime 
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_refresh_token_required
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)

@app.route('/api/users/register', methods=['POST'])
def register():
    users = mongo.db.users
    first_name = request.get_json()['data']['firstName']
    last_name = request.get_json()['data']['lastName']
    email = request.get_json()['data']['email']
    username = str(first_name) + str(last_name)
    password = bcrypt.generate_password_hash(request.get_json()['data']['password']).decode('utf-8')
    chat_rooms = []
    messages = []
    user_id = users.insert({
        'firstName': first_name,
        'lastName': last_name,
        'email': email,
        'password': password,
        'username': username,
        'chatRooms': chat_rooms,
        'messages': messages,
    })
    new_user = users.find_one({'_id': user_id})
    result = {'email': new_user['email'] + ' je registriran'}
    return jsonify({'Rezultat': result})

@app.route('/api/users/login', methods=['POST'])
def login():
    users = mongo.db.users
    email = request.get_json()['data']['email']
    password = request.get_json()['data']['password']
    result = ""

    response = users.find_one({'email': email})
    if response:
        if bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity= {
                'firstName': response['firstName'],
                'lastName': response['lastName'],
                'email': response['email'],
                'username': response['username'],
                'id': str(response['_id'])
            })
            result = jsonify({'token': access_token})
        else: 
            result = jsonify({'Error': 'Neispravna autentikacijska polja'})
    else:
        result = jsonify({'Rezultat': 'Nema rezultata'})
    return result

            # refresh_token = create_refresh_token(identity= {
            #     'firstName': response['firstName'],
            #     'lastName': response['lastName'],
            #     'email': response['email'],
            #     'username': response['username']
            # })