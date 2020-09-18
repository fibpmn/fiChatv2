from app import app
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from app import camundarest
from app import xmlparser
from app import dbroutes
from app import externals
from bson import BSON, json_util, ObjectId
from flask_cors import cross_origin
import requests, json, time, re, datetime

mongo = PyMongo(app)
CORS(app, resources={r'/*': {'origins': '*'}})

#pokreni instancu procesa
@app.route('/api/process-instance/<key>', methods=["POST"])
@cross_origin()
def start_instance(key):
    user = request.get_json()['username']
    process_name = request.get_json()['name']
    business_key = str(key) + str(user)
    
    try:
        data = json.loads(camundarest.start_process_instance_key(key, user, business_key))
        user_exists = list(mongo.db.users.find({"username": user}))[0]
    except Exception as error:
        return json.dumps({'Error': str(error)})                         
    try:
        room = {
            "name": process_name,
            "users": [user_exists['_id'], ObjectId("5f2ed1c620806f9c4fadc693")],
            "businessKey": data['businessKey'],
            "processInstanceId": data["id"],
            "definitionId": data["definitionId"],
            "variables": [],
            "flag": False,
            "initial": False,
            "active": True,
            "awaitingResponse": False,
            "awaitingResponseBy": ""
        }
        dbroutes.create_room(room)
    except Exception as e:
        return json.dumps({'Error': str(e)})
    return "Soba je kreirana"

@app.route('/api/<user>/task/variables', methods=["GET"])
@cross_origin()
def get_task_variables(user):
    
    if json.loads(dbroutes.get_selected_room(user)) != []:
        selected_room = json.loads(dbroutes.get_selected_room(user))[0]
        if selected_room['name'] == 'Recepcija' or selected_room == None:
            return "Nema pokrenutih procesa" 
        instance_id = selected_room['processInstanceId']
        definition_id = selected_room['definitionId']
        business_key = selected_room['businessKey']
        variables = selected_room['variables']
        flag = selected_room['flag']
        room_id = selected_room['_id']

        try:
            status = json.loads(camundarest.check_process_instance_status(instance_id, business_key, definition_id))[0]['state']
        except Exception as error:
            return json.dumps({'Error': str(error)})

        if status == 'ACTIVE':
            if camundarest.get_user_task(definition_id, instance_id) != '[]':
                try:
                    current_task = json.loads(camundarest.get_user_task(definition_id, instance_id))[0]
                    print("1")
                except Exception as error:
                    return json.dumps({'Error': str(error)})
                finally:           
                    task_form_key = current_task['formKey']
                    task_assignee = current_task['assignee']
            else:
                try:
                    current_task = json.loads(camundarest.get_external_task(definition_id, instance_id))[0]

                except Exception as error:
                    return json.dumps({'Error': str(error)})
                finally:
                    task_assignee = None
                    task_form_key = None
                    external_task_id = current_task['id']
                    external_topic_name = current_task['topicName']
                    external_worker_id = 'worker' + user

            if task_assignee != None:    

                if task_assignee == user:               
                    if task_form_key != None:
                        try:
                            print("2")
                            task_variables = xmlparser.parse(definition_id, task_form_key)
                        except Exception as error:
                            return {'Error': str(error)}    
                        if variables != []:
                            print("3")
                            if flag == False:
                                try:            
                                    print("4")  
                                    mongo.db.chatRooms.update_one({"_id": ObjectId(room_id['$oid'])}, {'$set': {'flag': True}})
                                except Exception as error:
                                    return json.dumps({'Error': str(error)})
                                finally:
                                    print("5")
                                    print("variables: ", variables)
                                    print("task_variables: ", task_variables)
                                    data = {
                                        "databaseVariables": variables,
                                        "serviceVariables": task_variables,
                                    }
                                    print("data: ", data)
                                    return data
                            else:                           
                                return task_variables
                        else:
                            return task_variables
                    else:
                        if variables != []:                               
                            if flag == False:                   
                                try:              
                                    mongo.db.chatRooms.update_one({"_id": ObjectId(room_id['$oid'])}, {'$set': {'flag': True}})
                                except Exception as error:
                                    return json.dumps({'Error': str(error)})
                                data = {
                                    "databaseVariables": variables,
                                    "serviceVariables": task_variables,
                                }
                                return data
                            else:                              
                                return "Chat logika" #Varijable su vec povucene iz baze
                        else:
                            return "Chat logika" #Varijable ne postoje
                else: 
                    return "Task mora odraditi druga osoba"

            else:
                if task_form_key != None:
                    return "Task mora odraditi druga osoba"
                else:
                    if external_topic_name == 'izracunaj_skolarinu':
                        response = externals.izracunaj_skolarinu(external_task_id, external_topic_name, external_worker_id, variables)
                    elif external_topic_name == 'upisi_studenta':
                        response = externals.upisi_studenta(external_task_id, external_topic_name, external_worker_id, variables, user)
                    elif external_topic_name == 'unos_prijave':
                        response = externals.unos_prijave(external_task_id, external_topic_name, external_worker_id, variables, user)
                    return response
        else:
            try:
                mongo.db.chatRooms.update_one({"_id": ObjectId(room_id['$oid'])}, {'$set': {'active': False}})
            except Exception as error:
                return json.dumps({'Error': str(error)})
            return "Proces je završen"
    else:
        return "Nema soba instanci za ovog korisnika"


@app.route('/api/<user>/task/variables', methods=['POST'])
@cross_origin()
def send_task_variables(user):
    data = request.get_json()
    selected_room = json.loads(dbroutes.get_selected_room(user))[0]
    instance_id = selected_room['processInstanceId']
    definition_id = selected_room['definitionId']
    room_id = selected_room['_id']
    current_task = json.loads(camundarest.get_user_task(definition_id, instance_id))[0]
    task_id = current_task['id']
    if data != []:
        instance_variables = data['variables'] 
        var_values = {
            '$addToSet': {
                "variables": instance_variables
            }
        }
        query = list(mongo.db.chatRooms.find({"_id": selected_room, "initial": False}))
        mongo.db.chatRooms.update_one({"_id": ObjectId(room_id['$oid'])}, var_values)

        #return camundarest.complete_user_task(task_id, instance_variables)
    else:
        instance_variables = None
        return camundarest.complete_user_task(task_id, instance_variables)

@app.route('/api/<user>/task/assignee', methods=['GET'])
@cross_origin()
def get_assignee(user):
    selected_room = json.loads(dbroutes.get_selected_room(user))[0]
    if selected_room['name'] == 'Recepcija' or selected_room == None:
        return "Nema pokrenutih procesa" 
    instance_id = selected_room['processInstanceId']
    definition_id = selected_room['definitionId']
    business_key = selected_room['businessKey']
    try:
        assignee = json.loads(camundarest.get_current_task_assignee(instance_id, business_key, definition_id))[0]['assignee']
    except Exception as error:
        return json.dumps({'Error': str(error)})
    return assignee

#DATABASE VARS INTO MESSAGES FORMATTER
@app.route('/api/<user>/task/variables/format', methods=['GET'])
@cross_origin()
def make_messages_out_of_database_variables(user):
    selected_room = mongo.db.users.find_one({"username": user})['selectedRoom']
    room = list(mongo.db.chatRooms.find({"_id": ObjectId(selected_room)}))[0]
    flag = room['flag']
    if flag != True:
        variable_names = []
        props_list = []
        for i in room['variables']: #prodi kroz varijable
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
        return json.dumps(messages, default=json_util.default, sort_keys=False)
    else:
        return "Varijable su iz baze vec povucene"




#FUNCTION USED IN VUE GENERATOR FOMR, NOT TO BE USED IN CHAT
#GET MENTORS 
@app.route('/api/mentors', methods=["GET"])
@cross_origin()
def get_mentors():
    profesori_object = mongo.db.groups.find_one({"name": "Profesori"})
    mentori = profesori_object['members']
    ime_prezime = []
    for i in range(len(mentori)):
        mentor_username = mongo.db.users.find_one({"_id": mentori[i]})['username']
        element = ''
        for i, slovo in enumerate(mentor_username):
            if i and slovo.isupper():
                element += ' '
            element += slovo
        ime_prezime.append(element)    
    temp = {"temp": ime_prezime}
    return temp

#GET TASK ID
@app.route('/api/task/complete/<username>', methods=['GET'])
@cross_origin()
def get_task_id_for_task_completion(username):
    user_object = mongo.db.users.find_one({"username": username})
    selected_room = user_object['selectedRoom'] 
    definition_id = mongo.db.chatRooms.find_one({"_id": ObjectId(selected_room)})['definitionId']
    instance_id = mongo.db.chatRooms.find_one({"_id": ObjectId(selected_room)})['processInstanceId']
    task = json.loads(camundarest.get_user_task(definition_id, instance_id))
    task_id = task[0]['id']
    return task_id

#COMPLETE TASK
@app.route('/api/task/complete/<id>', methods=["POST"])
@cross_origin()
def complete_user_task(id):
    data = request.get_json()
    user = data['username']
    selected_room = mongo.db.users.find_one({"username": user})['selectedRoom']
    mentor_username = data['variables']['Mentor']['value']
    mentor_oid = ObjectId(mongo.db.users.find_one({"username": mentor_username})['_id'])
    query = mongo.db.chatRooms.find_one({"_id": ObjectId(selected_room), "initial": False})['_id']
    values = {'$addToSet': {
        "users": mentor_oid
    }}
    mongo.db.chatRooms.update_one({"_id": query}, values)
    instance_variables = data['variables']
    var_values = {
        '$addToSet': {
            "variables": instance_variables
        }
    }
    mongo.db.chatRooms.update_one({"_id": query}, var_values)
    return camundarest.complete_user_task(id, instance_variables)

