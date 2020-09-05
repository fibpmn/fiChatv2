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
    print(key)
    user = request.get_json()['username'] #dobavi username s frontenda za camundu i bazu
    print(user)
    process_name = request.get_json()['name'] #dobavi ime procesa s frontenda za bazu
    print(process_name)
    data = json.loads(camundarest.start_process_instance_key(key, user)) #pokreni proces u camundi
    user_exists = list(mongo.db.users.find({"username": user})) #trazi usera u bazi
    if user_exists[0]['_id'] != None:                           #cudna mi je ova logika, ali radi
        try:
            room = {
             "name": process_name,
             "users": [user_exists[0]['_id']],
             "businessKey": data['businessKey'],
             "processInstanceId": data["id"],
             "definitionId": data["definitionId"],
             "variables": []
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
        task = json.loads(camundarest.get_user_task_form(definition_id, user))  #dobavi user task form key
        form_key = task[0]['formKey']                                                   #process form key za pronalazak user task forma u xmlu
        return xmlparser.parse(definition_id, form_key)
    else:
        return "Ok" #treba compleatati task ovdje

#posalji task varijable
@app.route('/api/task/complete/<assignee>')
@cross_origin()
def get_task_id_for_task_completion(assignee):
    user_object = mongo.db.users.find_one({"username": assignee})
    selected_room = user_object['selectedRoom'] 
    definition_id = mongo.db.chatRooms.find_one({"_id": ObjectId(selected_room)})['definitionId']
    task = json.loads(camundarest.get_user_task_form(definition_id, assignee))
    task_id = task[0]['id']
    return task_id

@app.route('/api/task/complete/<id>', methods=["POST"])
@cross_origin()
def complete_user_task(id):
    data = request.get_json()
    user = data['user']
    user_oid = ObjectId(mongo.db.users.find_one({"username": user})['_id'])
    mentor_username = data['variables']['Mentor']['value']
    mentor_oid = ObjectId(mongo.db.users.find_one({"username": mentor_username})['_id'])
    print(mentor_oid)
    #dodaj mentora u chatroom
    print(user_oid)
    query = ObjectId(mongo.db.chatRooms.find_one({"users": user_oid})['_id'])
    print(query)
    values = {'$addToSet': {
        "users": mentor_oid
    }}
    mongo.db.chatRooms.update_one({"_id": query}, values)
    #dodaj varijable u bazu
    instance_variables = data['variables']
    var_values = {
        '$addToSet': {
            "variables": instance_variables
        }
    }
    #'$push': {#"variables": { '$each': [instance_variables]}
    mongo.db.chatRooms.update_one({"_id": query}, var_values)
    return camundarest.complete_task(id, instance_variables)



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



# @app.route('/api/task/<assignee>', methods=["GET", "POST"])
# @cross_origin()
# def get_current_task(assignee):
#     if request.method == "GET":
#         ass = camundarest.get_task_list(assignee)
#         temp = json.loads(ass)
#         print(temp[0]['id'])
#         return camundarest.get_task_form_variables(temp[0]['id'])
#     else:
#         return "nesto"


# @app.route('/api/task/xml/<key>', methods=["GET"])
# @cross_origin()
# def get_xml(key):
#     if request.method == "GET":
#         return xmlparser.something(key)
#     else:
#         return "nesto"



# @app.route('/api/task/form', methods=["POST"])
# @cross_origin()
# def submit_task_form():
#     content = request.get_json()
#     print(content)
#     if request.method == "POST":
#         # user_task = camundarest.submit_form(content['id'], content['naslov'], content['sazetak'], content['dispozicija'], content['literatura'], content['obrazac'])
#         # tempuser_task = request.get_json(user_task)
#         #print(tempuser_task)
#         workerId = "workerId" + "ToniID" #user
#         #print(workerId)
#         time.sleep(2)
#         fetch = camundarest.fetch_and_lock(workerId, 1, 'submit_variables')
#         temp = json.loads(fetch)
#         #print(temp[0]['id'])
#         complete = camundarest.complete_external_task(temp[0]['id'], workerId, content['mentori'])
#         return "user_task, complete"
#     else:
#         return "pepe"


# @app.route('/api/send') , content['mentori']
# @cross_origin()
# def first_user_task():
#     content = request.get_json()
#     temp = json.dumps(content) #content je sada string
#     print(temp)
#     temp1 = json.loads(temp)
#     naslov = temp1['naslov']
#     sazetak = temp1['sazetak']
#     mentori_1 = temp1['mentori'][0]['value']
#     mentori_2 = temp1['mentori'][1]['value']
#     # variables = {
#     #     "Naslov": naslov,
#     #     "Sazetak": sazetak,
#     #     "Mentori":
#     # }
#     if request.method == 'POST':
#         camundarest.start_process_instance_key("PrijavaZavrsnogRada", "somethingNew", True)
#         print(naslov)
#         print(sazetak)
#         print(mentori_1)
#         print(mentori_2)
#         return "PEPE"
#     else:
#         varijable = request.get_json()
#         return varijable
        # Treba povuci usera jer je on prvi assignee na prvom tasku, to usera ukljuciti u poziv start instance u varijablama


# @app.route('/api/start-instance', methods=['POST', 'GET'])
# @cross_origin()
# def start_instance():
#     if request.method == 'POST':
#         camundarest.start_process_instance_key("PrijavaZavrsnogRada", "", False)
#         print("Something")
#         return "yas"
#     else:
#         return "Pepe"
    # print(varijable)
    # return varijable
