from app import app
from flask_pymongo import PyMongo
from bson import BSON, json_util, ObjectId
import datetime, json

mongo = PyMongo(app)

def parse_db_data(user, variables):
    print("User: ", user)
    selected_room = mongo.db.users.find_one({"username": user})['selectedRoom']
    #room = list(mongo.db.chatRooms.find({"_id": ObjectId(selected_room)}))[0]
    print("variables dbparser: ", variables)
    variable_names = []
    props_list = []
    for i in variables: #prodi kroz varijable
        variable_name = i.keys()       #uzmi nazive varijabli, pr. "NaslovRada"
        variable_props = i.values()       #uzmi svojstva varijable, pr. {"value": "blabla", "type": "String"}
        for index in variable_name:    
            element = ''
            for k, l in enumerate(index):           #ovo sluzi za stavljanje razmaka u usernameu, k je proslo slovo, l je trenutno slovo
                if k and l.isupper():
                    element += ' '
                element += l
            variable_names.append(element)              #dodaj element u polje varijabli imena 
        for index in variable_props:                        
            properties = (list(index.values())[0])             
            props_list.append(properties)               #dodaj element u polje varijabli svojstava

    #ovdje se konkateniraju imena i svojstva u jedan objekt koji se kasnije appenda u listu, 1 element liste = 1 message content
    object_concat = {}                                  
    list_of_content = []
    for index in range(len(variable_names)):
        object_concat = str(variable_names[index]) + ": " + str(props_list[index]) #ovo je content
        list_of_content.append(object_concat)

    messages = []
    temporary = {}
    sender_id = mongo.db.users.find_one({"username": "Fi"})["_id"]
    room_id = selected_room
    timestamp = datetime.datetime.now().isoformat() + "Z"

    for key in range(len(list_of_content)):
        temporary = {
            "room_id": room_id,
            "sender_id": sender_id,
            "username": "Fi",
            "content": list_of_content[key],
            "timestamp": timestamp,
            "seen": False
        }
        messages.append(temporary)
    return json.dumps(messages, default=str)#, sort_keys=False)