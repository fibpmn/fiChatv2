from app import app
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_cors import cross_origin
from app import camundarest
from bson import BSON, json_util, ObjectId
from flask_pymongo import PyMongo
import json

mongo = PyMongo(app)

#for external tasks, mock some services
def izracunaj_skolarinu(external_task_id, external_task_topic, external_task_worker, variables, user):
    user_exists = list(mongo.db.users.find({"username": user}))[0]
    selected_room = ObjectId(user_exists['selectedRoom'])
    room_id = list(mongo.db.chatRooms.find({"_id": selected_room}))[0]
    print("User Exists: ", user_exists)
    status = variables['value']
    iznos_skolarine = 0
    if status == 'izvanredni':
        iznos_skolarine = 5000 
    elif status == 'ponavljac':
        iznos_skolarine = 5500
    else:
        iznos_skolarine = 5500
    variables = {"Skolarina": {"value": iznos_skolarine,
                               "type": "long"
    }}
    var_values = {
    '$addToSet': {
        "variables": variables
        }
    }
    mongo.db.chatRooms.insert_one({"_id": ObjectId(room_id)}, var_values)
    resp = camundarest.complete_external_task(external_task_id, external_task_worker, variables)        
    return resp

def upisi_studenta(external_task_id, external_task_topic, external_task_worker, variables, user):
    user_exists = list(mongo.db.users.find({"username": user}))[0]
    print("User Exists: ", user_exists)
    first_name = user_exists['firstName']
    last_name = user_exists['lastName']
    email = user_exists['email']
    selected_room = ObjectId(user_exists['selectedRoom'])
    room = list(mongo.db.chatRooms.find({"_id": selected_room}))[0]
    print("Odabrana soba: ", selected_room)
    for room_variables in room['variables']:
        variables = room_variables
    data = {
        "type": "Upis na diplomski studij",
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "variables": variables
    }
    mongo.db.submittedApplications.insert_one(data)
    camundarest.fetch_and_lock(external_task_worker, external_task_topic)
    req = camundarest.complete_external_task(external_task_id, external_task_worker, variables)
    return req

def unos_prijave(external_task_id, external_task_topic, external_task_worker, variables, user):
    user_exists = list(mongo.db.users.find({"username": user}))[0]
    print("User Exists: ", user_exists)
    first_name = user_exists['firstName']
    last_name = user_exists['lastName']
    email = user_exists['email']
    selected_room = ObjectId(user_exists['selectedRoom'])
    print("Odabrana soba: ", selected_room)
    room = list(mongo.db.chatRooms.find({"_id": selected_room}))[0]
    for room_variables in room['variables']:
        variables = room_variables
    data = {
        "type": "Prijava zavrsnog rada",
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "variables": variables
    }
    mongo.db.submittedApplications.insert_one(data)
    camundarest.fetch_and_lock(external_task_worker, external_task_topic)
    req = camundarest.complete_external_task(external_task_id, external_task_worker, variables)
    return req #"Čestitamo! Uspješno ste prijavili završni rad"