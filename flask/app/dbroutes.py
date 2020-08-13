import json
from app import app
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import BSON, json_util
from flask_cors import cross_origin
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager
# from flask_jwt_extended import create_access_token

mongo = PyMongo(app)

@app.route('/')
def index():
    return 'Not good for you.'

@app.route('/api/getRefs', methods=['GET'])
def getRefs():
    usersRef = mongo.db.users
    roomsRef = mongo.db.chatRooms
    filesRef = mongo.db.files
    return json.dumps(mongo.db.chatRooms.find_one(), sort_keys=True, indent=4, default=json_util.default)
