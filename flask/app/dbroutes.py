import json
from app import app
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import BSON, json_util, ObjectId
from flask_cors import cross_origin
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager
# from flask_jwt_extended import create_access_token

mongo = PyMongo(app)

@app.route('/')
def index():
    return 'good for you.'

#sve sobe
@app.route('/api/getRooms', methods=['GET'])
def getRooms():
    try:
        docs_list = list(mongo.db.chatRooms.find())
        return json.dumps(docs_list, default=json_util.default)
    except Exception as e:
        return json.dumps({'error' : str(e)})


#svi useri
@app.route('/api/getUsers', methods=['GET'])
def getUsers():
    try:
        docs_list = list(mongo.db.users.find())
        return json.dumps(docs_list, default=json_util.default)
    except Exception as e:
        return json.dumps({'error' : str(e)})


#sve poruke
@app.route('/api/getMessages', methods=['GET'])
def getMessages():
    try:
        docs_list = list(mongo.db.messages.find())
        return json.dumps(docs_list, default=json_util.default)
    except Exception as e:
        return json.dumps({'error' : str(e)})


#sve poruke određene sobe
@app.route('/api/getRoomMessages/<room_id>', methods=['GET'])
def getRoomMessages(room_id):
    try:
        docs_list = list(mongo.db.messages.find({
        "room_id" : ObjectId(room_id)
        }))
        return json.dumps(docs_list, default=json_util.default)
    except Exception as e:
        return json.dumps({'error' : str(e)})

#sve poruke određenog user
@app.route('/api/getUserMessages/<user_id>', methods=['GET'])
def getUserMessages(user_id):
    try:
        docs_list = list(mongo.db.messages.find({
        "sender_id" : ObjectId(user_id)
        }))
        return json.dumps(docs_list, default=json_util.default)
    except Exception as e:
        return json.dumps({'error' : str(e)})


#sobe u kojima je user
@app.route('/api/getUserRooms/<user_id>', methods=['GET'])
def getUserRooms(user_id):
    try:
        docs_list = list(mongo.db.chatRooms.find({
        "users" : ObjectId(user_id)
        }))
        return json.dumps(docs_list, default=json_util.default)
    except Exception as e:
        return json.dumps({'error' : str(e)})
