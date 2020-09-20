from app import app
from flask_pymongo import PyMongo
from bson import BSON, json_util, ObjectId
import datetime, json

mongo = PyMongo(app)

def parse_db_data(user, variables):

    selected_room = mongo.db.users.find_one({"username": user})['selectedRoom']
    variable_names = []
    props_list = []
    variables = list(filter(None, variables))
    for i in variables:
        variable_name = i.keys()      
        variable_props = i.values()       
        for index in variable_name:    
            element = ''
            for k, l in enumerate(index):           
                if k and l.isupper():
                    element += ' '
                element += l
            variable_names.append(element)         
        for index in variable_props:                        
            properties = (list(index.values())[0])             
            props_list.append(properties)   

    
    object_concat = {}                                  
    list_of_content = []
    for index in range(len(variable_names)):
        object_concat = str(variable_names[index]) + ": " + str(props_list[index])
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
    return json.dumps(messages, default=str)