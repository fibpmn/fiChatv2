from app import app
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from app import camundarest
from app import xmlparser
from app import dbroutes
from bson import BSON, json_util, ObjectId
from flask_cors import cross_origin
import requests, json, time, re

mongo = PyMongo(app)
CORS(app, resources={r'/*': {'origins': '*'}})

#pokreni instancu procesa
@app.route('/api/process-instance/<key>', methods=["POST"])
@cross_origin()
def start_instance(key):
    user = request.get_json()['username'] 
    data = json.loads(camundarest.start_process_instance_key(key, user)) 
    user_exists = list(mongo.db.users.find({"username": user})) 
    process_name = request.get_json()['name']
    if user_exists[0]['_id'] != None:                          
        try:
            room = {
             "name": process_name,
             "users": [user_exists[0]['_id']],
             "businessKey": data['businessKey'],
             "processInstanceId": data["id"],
             "definitionId": data["definitionId"],
             "variables": [],
             "flag": False,
            }
            dbroutes.create_room(room)
        except Exception as e:
            return json.dumps({'Error': str(e)})
    else: 
        return "Korisnik ne postoji"
    return "ok"

#vrati task varijable
@app.route('/api/task/<user>', methods=["GET"])
@cross_origin()
def user_task_form(user):
    if request.method == "GET":
        user_object = mongo.db.users.find_one({"username": user})
        selected_room = user_object['selectedRoom'] 
        definition_id = mongo.db.chatRooms.find_one({"_id": ObjectId(selected_room)})['definitionId']
        task = json.loads(camundarest.get_user_task_form(definition_id, user))  
        form_key = task[0]['formKey']                                                
        return xmlparser.parse(definition_id, form_key)
    else:
        return "Ok"

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

#posalji task varijable
@app.route('/api/task/complete/<username>')
@cross_origin()
def get_task_id_for_task_completion(username):
    user_object = mongo.db.users.find_one({"username": username})
    selected_room = user_object['selectedRoom'] 
    definition_id = mongo.db.chatRooms.find_one({"_id": ObjectId(selected_room)})['definitionId']
    task = json.loads(camundarest.get_user_task_form(definition_id, username))
    task_id = task[0]['id']
    return task_id

@app.route('/api/task/complete/<id>', methods=["POST"])
@cross_origin()
def complete_user_task(id):
    data = request.get_json()
    print(data)
    user = data['username']
    user_oid = mongo.db.users.find_one({"username": user})['_id']
    mentor_username = data['variables']['Mentor']['value']
    mentor_oid = ObjectId(mongo.db.users.find_one({"username": mentor_username})['_id'])
    query = ObjectId(mongo.db.chatRooms.find_one({"users": user_oid})['_id'])
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
    return camundarest.complete_task(id, instance_variables)



@app.route('/api/task/state/<user>', methods=["GET"])
@cross_origin()
def check_state(user):
    user_oid = mongo.db.users.find_one({"username": user})['_id']
    user_in_rooms = list(mongo.db.chatRooms.find({'users': user_oid}))
    if user_in_rooms != '[]':
        print(user_in_rooms)
        iterator = 0
        for room_id in user_in_rooms:
            current_tasks = json.loads(camundarest.get_current_task(room_id['definitionId'], room_id['processInstanceId']))
            print("Current tasks: ", current_tasks)
            if current_tasks[iterator]['assignee'] == user: #"Je li user assignee u nekom od chatrooma?"
                task_id = current_tasks[iterator]['id']
                print("\n")
                print("TaskID: ", task_id)
                definition_id = current_tasks[iterator]['processDefinitionId']
                print("DefinitionID: ", definition_id)
                form_key = current_tasks[iterator]['formKey']
                print("FormKey: ", form_key)
                if form_key != "": #
                    camunda_variables = current_tasks
                    mongo_variables = user_in_rooms[iterator]['variables']
                    print(mongo_variables)
                    if mongo_variables == '[]':
                        print("1. Incomplete task")
                        return xmlparser.parse(camunda_variables[iterator]['processDefinitionId'], camunda_variables[iterator]['formKey'])
                    else: 
                        mongo_flag = user_in_rooms[iterator]['flag']
                        if mongo_flag == False:
                            flag_value = {'$set': {
                                'flag': True
                            }}
                            mongo.db.chatRooms.update_one({"_id": user_in_rooms[iterator]['_id']}, flag_value)
                            camunda_variables = xmlparser.parse(camunda_variables[iterator]['processDefinitionId'], camunda_variables[iterator]['formKey'])
                            print("Mongo:", mongo_variables)
                            print("Camunda:", camunda_variables)
                            data = {
                                "databaseVariables": mongo_variables,
                                "camundaVariables": camunda_variables
                            }
                            print("2. Incomplete task")
                            return data
                        else:
                            print("3. Incomplete task")
                            return xmlparser.parse(camunda_variables[iterator]['processDefinitionId'], camunda_variables[iterator]['formKey'])
                else:
                    mongo_flag = user_in_rooms[iterator]['flag']
                    if mongo_flag == False:
                        flag_value = {'$set': {
                                'flag': True
                        }}
                        mongo.db.chatRooms.update_one({"_id": user_in_rooms[iterator]['_id']}, flag_value)
                        mongo_variables = user_in_rooms[iterator]['variables']
                        print("4. Incomplete task")
                        return mongo_variables
                    else:
                        print("5. Chat logika, vidjet cemo jos sto je to")
                        return "Chat/Chatbot logika"
            else:
                if current_tasks[iterator]['assignee'] != "null":
                    print("6. Incomplete task")
                    return "Task has to be done by someone else"
                else:
                    #GetExternalTask -> name
                    #IzvršiExternalTask
                    #MozdaICompleteTask
                    print("pepe")
                    return "pepe"
        iterator += 1
    return "Korisnik se ne nalazi u nijednoj chat sobi"
