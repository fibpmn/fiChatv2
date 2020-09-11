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
    return 'Not good for you.'

# sve sobe
@app.route('/api/getRooms', methods=['GET'])
def getRooms():
    try:
        docs_list = list(mongo.db.chatRooms.find())
        return json.dumps(docs_list, default=json_util.default)
    except Exception as e:
        return json.dumps({'error': str(e)})

#predsoblje
@app.route('/api/fiRoom', methods=['POST'])
@cross_origin()
def create_fi_room():
    try:
        data = request.get_json()
        user_email = data['email'] 
        fi_email = data['fiemail']
        room_name = data['name']
        user = list(mongo.db.users.find({"email": user_email})) 
        print(user)
        fi = list(mongo.db.users.find({"email": fi_email})) 
        print(fi)
        room = {
             "name": room_name,
             "users": [user[0]['_id'], fi[0]['_id']],
             "businessKey": "",
             "processInstanceId": "",
             "definitionId": "",
             "variables": []
        }
        mongo.db.chatRooms.insert_one(room)
        return "ok"
    except Exception as e:
        return json.dumps({'Error': str(e)})

# sobe usera
@app.route('/api/getUserRooms/<user_id>', methods=['GET'])
def getUserRooms(user_id):
    try:
        docs_list = list(mongo.db.chatRooms.find({
            "users": ObjectId(user_id)
        }))
        return json.dumps(docs_list, default=json_util.default)
    except Exception as e:
        return json.dumps({'error': str(e)})

# svi useri
@app.route('/api/getUsers', methods=['GET'])
def getUsers():
    try:
        docs_list = list(mongo.db.users.find())
        return json.dumps(docs_list, default=json_util.default)
    except Exception as e:
        return json.dumps({'error': str(e)})

# uzmi za jednog usera
@app.route('/api/getUserData/<user_id>', methods=['GET'])
def getUserData(user_id):
    try:
        docs_list = list(mongo.db.users.find({
            "_id": ObjectId(user_id)
        }))
        return json.dumps(docs_list, default=json_util.default)
    except Exception as e:
        return json.dumps({'error': str(e)})

# updejtaj field korisnika
@app.route('/api/updateUserField', methods=['POST'])
@cross_origin()
def updateUserField():
    try:
        data = request.get_json()
        user_id = ObjectId(data["user"])
        values = {'$set': {
            data["field"]: data["value"]
        }}
        query = {"_id": user_id}
        mongo.db.users.update_one(query, values)
        return "ok"
    except Exception as e:
        return json.dumps({'error': str(e)})

# sve poruke
@app.route('/api/getMessages', methods=['GET'])
def getMessages():
    try:
        docs_list = list(mongo.db.messages.find())
        return json.dumps(docs_list, default=json_util.default)
    except Exception as e:
        return json.dumps({'error': str(e)})

# dodaj poruku
@app.route('/api/addMessage', methods=['POST'])
@cross_origin()
def addMessage():
    try:
        data = request.get_json()
        data["sender_id"] = ObjectId(data["sender_id"])
        data["room_id"] = ObjectId(data["room_id"])
        mongo.db.messages.insert_one(data)
        return "ok"
    except Exception as e:
        return json.dumps({'error': str(e)})

# updejtaj field poruke
@app.route('/api/updateMessageField', methods=['POST'])
@cross_origin()
def updateMessageField():
    try:
        data = request.get_json()
        room_id = ObjectId(data["room"])
        values = {'$set': {
            data["field"]: data["value"]
        }}
        query = {"room_id": room_id}
        mongo.db.messages.update_many(query, values)
        return "ok"
    except Exception as e:
        return json.dumps({'error': str(e)})

# sve poruke određenog usera
@app.route('/api/getUserMessages/<user_id>', methods=['GET'])
def getUserMessages(user_id):
    try:
        docs_list = list(mongo.db.messages.find({
            "sender_id": ObjectId(user_id)
        }))
        return json.dumps(docs_list, default=json_util.default)
    except Exception as e:
        return json.dumps({'error': str(e)})

# sve poruke određene sobe
@app.route('/api/getRoomMessages/<room_id>', methods=['GET'])
def getRoomMessages(room_id):
    try:
        docs_list = list(mongo.db.messages.find({
            "room_id": ObjectId(room_id)
        }).sort("timestamp", 1))
        return json.dumps(docs_list, default=json_util.default)
    except Exception as e:
        return json.dumps({'error': str(e)})

# uzmi zadnju poruku određene sobe
@app.route('/api/getLastRoomMessage/<room_id>', methods=['GET'])
def getLastRoomMessage(room_id):
    try:
        docs_list = list(mongo.db.messages.find({
            "room_id": ObjectId(room_id)
        }).sort("timestamp", -1).limit(1))
        return json.dumps(docs_list, default=json_util.default)
    except Exception as e:
        return json.dumps({'error': str(e)})

################### bpmn

@app.route('/api/room', methods=['POST'])
@cross_origin()
def create_room(room):
    try:
        mongo.db.chatRooms.insert_one(room)
        print("Soba je kreirana")
        return "ok"
    except Exception as e:
        return json.dumps({'Error': str(e)})


@app.route('/api/process-definitions', methods=["GET"])
def get_processes():
    if request.method == "GET":
        docs_list = list(mongo.db.processes.find())
        print(docs_list)
        return json.dumps(docs_list, default=json_util.default)

@app.route('/api/userinrooms', methods=["GET"])
def get_selected_room(user):
    try:
        selected_room = mongo.db.users.find_one({"username": user})['selectedRoom']
        room = list(mongo.db.chatRooms.find({"_id": ObjectId(selected_room)}))
        return json.dumps(room, default=json_util.default)
    except Exception as e:
        return json.dumps({'Error': str(e)})

@app.route('/api/task/variables', methods=["GET"])
def set_flag(id):
    try:
        flag_value = {'$set': {
                        'flag': True
        }}
        mongo.db.chatRooms.update_one({"_id": id}, flag_value)
        return "Flag set to true"
    except Exception as e:
        return json.dumps({'Error': str(e)})