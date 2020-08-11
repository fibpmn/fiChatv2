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

#sve sobe, ili ako je dan userid, po useridu
@app.route('/api/getRooms')
@app.route('/api/getRooms/<userid>', methods=['GET'])
def getRooms(userid=None):
    if userid is None:
        docs_list = list(mongo.db.chatRooms.find())
    else:
        docs_list = list(mongo.db.chatRooms.find({
        "users" : ObjectId(userid)
        }))
    return json.dumps(docs_list, default=json_util.default)

#sve poruke, ili ako je dan userid, po useridu
@app.route('/api/getMessages')
@app.route('/api/getMessages/<userid>', methods=['GET'])
def getMessages(userid=None):
    if userid is None:
        docs_list = list(mongo.db.messages.find())
    else:
        docs_list = list(mongo.db.messages.find({
        "sender_id" : ObjectId(userid)
        }))
    return json.dumps(docs_list, default=json_util.default)

#sve poruke po sobama