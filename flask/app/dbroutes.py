from app import app
from flask import jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/')
def index():
    return 'good for you.'

@app.route('/api/getRefs', methods=['GET'])
def getRefs():
    usersRef = mongo.db.users
    roomsRef = mongo.db.chatRooms
    filesRef = mongo.db.files
    return 'got the refs'