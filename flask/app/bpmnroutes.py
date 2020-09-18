from app import app
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from app import camundarest
from app import xmlparser
from app import dbroutes
from app import externals
from app import dbparser
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
        print("Odabrana soba, moze doci do problema kada profesor ima dvije prijave zavrsnog: ", selected_room)
        if selected_room['name'] == 'Recepcija' or selected_room == None:
            return "Nema pokrenutih procesa" 
        instance_id = selected_room['processInstanceId']
        definition_id = selected_room['definitionId']
        business_key = selected_room['businessKey']
        variables = json.loads(dbparser.parse_db_data(user, selected_room['variables']))
        print("Ovdje izlaze DB varijable za front: ", variables)
        flag = selected_room['flag']
        room_id = selected_room['_id']
        print("Flag odabrane sobe: ", flag)
        print("Room_ID odabrane sobe: ", room_id)
        try:
            status = json.loads(camundarest.check_process_instance_status(instance_id, business_key, definition_id))[0]['state']
            print("Provjera statusa procesne instance, ako je ACTIVE, nastavi s radom: ", status)
        except Exception as error:
            return json.dumps({'Error': str(error)})

        if status == 'ACTIVE':
            if camundarest.get_user_task(definition_id, instance_id) != '[]':
                try:
                    current_task = json.loads(camundarest.get_user_task(definition_id, instance_id))[0]
                    print("Provjera jel trenutni task- User task")
                except Exception as error:
                    return json.dumps({'Error': str(error)})
                finally:           
                    task_form_key = current_task['formKey']
                    task_assignee = current_task['assignee']
            else:
                try:
                    current_task = json.loads(camundarest.get_external_task(definition_id, instance_id))[0]
                    print("Provjera jel trenutni task- External task")
                except Exception as error:
                    return json.dumps({'Error': str(error)})
                finally:
                    task_assignee = None
                    task_form_key = None
                    external_task_id = current_task['id']
                    external_topic_name = current_task['topicName']
                    external_worker_id = 'worker' + user

            if task_assignee != None:    
                print("Task Assignee postoji")
                if task_assignee == user:
                    print("Task Assignee je User")               
                    if task_form_key != None:
                        try:
                            print("Task Form Key postoji, što znači da postoje varijable u Camundi koje treba preuzeti")
                            task_variables = json.loads(xmlparser.parse(definition_id, task_form_key))
                        except Exception as error:
                            return {'Error': str(error)}    
                        if variables != []:
                            print("Varijable u bazi nisu prazne, pa slijedi provjera")
                            if flag == False:
                                try:            
                                    print("Flag je false što znači da ce povuci te varijable iz baze samo jednom")  
                                    mongo.db.chatRooms.update_one({"_id": ObjectId(room_id['$oid'])}, {'$set': {'flag': True}})
                                except Exception as error:
                                    return json.dumps({'Error': str(error)})
                                finally:
                                    data = {
                                        "databaseVariables": variables,
                                        "serviceVariables": task_variables,
                                    }
                                    print("Vraca i DB i Camunda varijable: ", data)
                                    return data
                            else:
                                print("Varijable iz baze su povucene, pa vraca samo one iz Camunde: ", task_variables)                        
                                return task_variables
                        else:
                            #Ovo ce se vjerojatno izvrsiti samo jedanput
                            print("Varijable u bazi su prazne, pa vraca samo one iz Camunde: ", task_variables)
                            return task_variables
                    else:
                        print("Form Key je prazan sto znaci da nema varijabli u Camundi")
                        if variables != []:
                            print("Provjera jel Flag == false")                               
                            if flag == False:
                                print("Varijable u Camundi su prazne, ali je doslo do ovdje kako bi uzeo varijable iz Baze- skoro pa edgecase")                  
                                try:              
                                    mongo.db.chatRooms.update_one({"_id": ObjectId(room_id['$oid'])}, {'$set': {'flag': True}})
                                except Exception as error:
                                    return json.dumps({'Error': str(error)})
                                finally:
                                    return variables
                            else:
                                print("Totalni edgecase, u Camundi su prazne varijable, a iz Baze vec povucene")                              
                                return "Chat logika" #Varijable su vec povucene iz baze
                        else:
                            print("Osim sto su u Camundi prazne varijable, prazne su i u bazi. To je onaj task gdje profesor i student chataju")
                            return "Chat logika" #Varijable ne postoje
                else:
                    print("Trenutno ulogirani korisnik nije assignee")
                    return "Task mora odraditi druga osoba"

            else:
                print("Assignee ne postoji, sto znaci da trenutni user nije assignee ili da je external task")
                if task_form_key != None:
                    print("Trenutno ulogirani korisnik nije assignee")
                    return "Task mora odraditi druga osoba"
                else:
                    print("Trentuni task radi stroj, tj. task je external")
                    if external_topic_name == 'izracunaj_skolarinu':
                        response = externals.izracunaj_skolarinu(external_task_id, external_topic_name, external_worker_id, variables)
                    elif external_topic_name == 'upisi_studenta':
                        response = externals.upisi_studenta(external_task_id, external_topic_name, external_worker_id, variables, user)
                    elif external_topic_name == 'unos_prijave':
                        response = externals.unos_prijave(external_task_id, external_topic_name, external_worker_id, variables, user)
                    return response
        else:
            print("Proces je zavsen i nema vise taskova")
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
        print("Camunda vars: ", instance_variables)
        var_values = {
            '$addToSet': {
                "variables": instance_variables
            }
        }
        #query = list(mongo.db.chatRooms.find({"_id": selected_room, "initial": False}))
        mongo.db.chatRooms.update_one({"_id": ObjectId(room_id['$oid'])}, var_values)
        return camundarest.complete_user_task(task_id, instance_variables)
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

#USED FOR VUE-GENERATOR, NOT TO BE USED IN CHAT
@app.route('/api/<user>/task/form/complete', methods=['POST'])
@cross_origin()
def complete_task_form(user):
    data = request.get_json()
    variables = data['variables']
    selected_room = json.loads(dbroutes.get_selected_room(user))[0]
    room_id = selected_room['_id']
    process_definition_id = selected_room['definitionId'] 
    process_instance_id = selected_room['processInstanceId']
    task_id = json.loads(camundarest.get_user_task(process_definition_id, process_instance_id))[0]['id']
 
    try:
        mentor_username = data['variables']['Mentor']['value']
        mentor_oid = ObjectId(mongo.db.users.find_one({"username": mentor_username})['_id'])
        query = mongo.db.chatRooms.find_one({"_id": ObjectId(room_id['$oid']), "initial": False})['_id']
        
        values = {'$addToSet': {
            "users": mentor_oid
        }}
        mongo.db.chatRooms.update_one({"_id": query}, values)

        var_values = {
            '$addToSet': {
                "variables": variables
            }
        }
        mongo.db.chatRooms.update_one({"_id": query}, var_values)
    except Exception as error:
        return json.dumps({"Error": str(error)})

    return camundarest.complete_user_task(task_id, variables)


