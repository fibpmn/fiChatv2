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
    business_key = str(key) + str(user)
    data = json.loads(camundarest.start_process_instance_key(key, user, business_key))
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
    if camundarest.get_user_task(definition_id, instance_id) != '[]':
        current_task = json.loads(camundarest.get_user_task(definition_id, instance_id))[0]
        task_id = current_task['id']
        task_form_key = current_task['formKey']
        task_assignee = current_task['assignee']
    else: 
        current_task = json.loads(camundarest.get_external_task(definition_id, instance_id))[0]
        task_id = current_task['id']
        task_assignee = None
        task_form_key = None
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
            print(external_task_id)
            # if external_topic_name == 'test':
            #     response = externals.test(external_task_id, external_topic_name, external_worker_id)
            # elif external_topic_name == 'izracunaj_skolarinu':
            #     #tu ce biti i varijable iz camunde, tip studenta
            #     response = externals.izracunaj_skolarinu()
            # elif external_topic_name == 'upisi_studenta':
            #     #takoder ce se slati varijable
            #     response = externals.upisi_studenta()
            # elif external_topic_name == 'unos_prijave':
            #     #ista stvar
            #     response = externals.unos_prijave()
            return "pepe"


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
@app.route('/api/task/complete/<username>')
@cross_origin()
def get_task_id_for_task_completion(username):
    user_object = mongo.db.users.find_one({"username": username})
    selected_room = user_object['selectedRoom'] 
    definition_id = mongo.db.chatRooms.find_one({"_id": ObjectId(selected_room)})['definitionId']
    instance_id = mongo.db.chatRooms.find_one({"_id": ObjectId(selected_room)})['instanceId']
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

