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
             "initial": False,
             "active": True,
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
    user = data['username']
    selected_room = mongo.db.users.find_one({"username": user})['selectedRoom']
    #print("Selected Room: ", selected_room)
    mentor_username = data['variables']['Mentor']['value']
    mentor_oid = ObjectId(mongo.db.users.find_one({"username": mentor_username})['_id'])
    query = mongo.db.chatRooms.find_one({"_id": ObjectId(selected_room), "initial": False})['_id']
    #print("Query: ", query)
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
    selected_room = json.loads(dbroutes.get_selected_room(user))[0]
    instance_id = selected_room['processInstanceId']
    definition_id = selected_room['definitionId']
    variables = selected_room['variables']
    flag = selected_room['flag']
    room_id = selected_room['_id']
    print("Selected room: ", selected_room)
    
    #current_task = json.loads(camundarest.get_current_task(definition_id, instance_id))[0]
    if camundarest.get_current_task(definition_id, instance_id) != '[]':
        current_task = json.loads(camundarest.get_current_task(definition_id, instance_id))[0]
        task_id = current_task['id']
        task_form_key = current_task['formKey']
        task_assignee = current_task['assignee']
    else: 
        current_task = json.loads(camundarest.get_current_external_task(definition_id, instance_id))[0]
        task_id = current_task['id']
        task_assignee = None
        task_form_key = None
    print(current_task)

    if task_assignee != None:
        if task_form_key != None:
            task_variables = xmlparser.parse(definition_id, task_form_key)
            if variables != []:
                if flag == False:
                    dbroutes.set_flag(room_id)
                    data = { 
                        "databaseVariables": variables,
                        "serviceVariables": task_variables,
                    }
                    return task_variables
                else:
                    return task_variables                
            else:
                return task_variables
        else:
            if flag == False:
                    dbroutes.set_flag(room_id)
                    data = {
                        "databaseVariables": variables,
                        "serviceVariables": task_variables,
                    }
                    return data
            else: 
                return "Chat logika"
    else:
        if task_form_key != None:
            return "Task mora odraditi druga osoba"
        else:
            external_task_id = task_id
            external_topic_name = current_task['topicName']
            external_worker_id = 'worker' + user
            if external_topic_name == 'test':
                response = externals.test(external_task_id, external_topic_name, external_worker_id)
            elif external_topic_name == 'izracunaj_skolarinu':
                #tu ce biti i varijable iz camunde, tip studenta
                response = externals.izracunaj_skolarinu()
            elif external_topic_name == 'upisi_studenta':
                #takoder ce se slati varijable
                response = externals.upisi_studenta()
            elif external_topic_name == 'unos_prijave':
                #ista stvar
                response = externals.unos_prijave()
            return "pepe"

    # if user_in_rooms != '[]':
    #     print("MONGO: ", user_in_rooms)
    #     print("\n")
    #     iterator = 0
    #     for room_id in user_in_rooms:
    #         print(user_in_rooms[iterator]['initial'])
    #         if user_in_rooms[iterator]['initial'] == False:
    #             current_tasks = json.loads(camundarest.get_current_task(room_id['definitionId'], room_id['processInstanceId']))
    #             print("CURRENT TASKS: ", current_tasks)
    #             if current_tasks[iterator]['assignee'] == user:
    #                 task_id = current_tasks[iterator]['id']
    #                 definition_id = current_tasks[iterator]['processDefinitionId']
    #                 form_key = current_tasks[iterator]['formKey']
    #                 if form_key != "": 
    #                     camunda_variables = current_tasks
    #                     mongo_variables = user_in_rooms[iterator]['variables']
    #                     print(mongo_variables)
    #                     if mongo_variables == '[]':
    #                         print("1. Incomplete task")
    #                         return xmlparser.parse(camunda_variables[iterator]['processDefinitionId'], camunda_variables[iterator]['formKey'])
    #                     else: 
    #                         mongo_flag = user_in_rooms[iterator]['flag']
    #                         if mongo_flag == False:
    #                             flag_value = {'$set': {
    #                                 'flag': True
    #                             }}
    #                             mongo.db.chatRooms.update_one({"_id": user_in_rooms[iterator]['_id']}, flag_value)
    #                             camunda_variables = xmlparser.parse(camunda_variables[iterator]['processDefinitionId'], camunda_variables[iterator]['formKey'])
    #                             print("Mongo:", mongo_variables)
    #                             print("Camunda:", camunda_variables)
    #                             data = {
    #                                 "databaseVariables": mongo_variables,
    #                                 "camundaVariables": camunda_variables
    #                             }
    #                             print("2. Incomplete task")
    #                             return data
    #                         else:
    #                             print("3. Incomplete task")
    #                             return xmlparser.parse(camunda_variables[iterator]['processDefinitionId'], camunda_variables[iterator]['formKey'])
    #                 else:
    #                     mongo_flag = user_in_rooms[iterator]['flag']
    #                     if mongo_flag == False:
    #                         flag_value = {'$set': {
    #                                 'flag': True
    #                         }}
    #                         mongo.db.chatRooms.update_one({"_id": user_in_rooms[iterator]['_id']}, flag_value)
    #                         mongo_variables = user_in_rooms[iterator]['variables']
    #                         print("4. Incomplete task")
    #                         return mongo_variables
    #                     else:
    #                         print("5. Chat logika, vidjet cemo jos sto je to")
    #                         return "Chat/Chatbot logika"
    #             else:
    #                 if current_tasks[iterator]['assignee'] != "null":
    #                     print("6. Incomplete task")
    #                     return "Task has to be done by someone else"
    #                 else:
    #                     #GetExternalTask -> name
    #                     #IzvršiExternalTask
    #                     #MozdaICompleteTask
    #                     print("pepe")
    #                     return "pepe"
    #         else:
    #             print("Else")
    #             print(iterator)
    #             iterator += 1
    #             continue

    #return "Korisnik se ne nalazi u nijednoj chat sobi"
