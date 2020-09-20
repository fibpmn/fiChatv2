from app import app
from app import camundarest
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from bson import BSON, json_util, ObjectId
import json, time

mongo = PyMongo(app)

#for external tasks, mock some services
def izracunaj_skolarinu(external_task_id, external_task_topic, external_task_worker, variables, user):

    user_exists = list(mongo.db.users.find({"username": user}))[0]
    selected_room = ObjectId(user_exists['selectedRoom'])
    status = ""
    for var in variables:
        if "true" in var['content']:
            status = var['content']

    iznos_skolarine = 0
    if 'izvanredni' in status:
        iznos_skolarine = 5000 
    elif 'ponavljac' in status:
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
    mongo.db.chatRooms.update_one({"_id": selected_room}, var_values)
    camundarest.fetch_and_lock(external_task_worker, external_task_topic)
    time.sleep(1)
    req = camundarest.complete_external_task(external_task_id, external_task_worker, variables)      
    return req

def upisi_studenta(external_task_id, external_task_topic, external_task_worker, variables, user):

    user_exists = list(mongo.db.users.find({"username": user}))[0]
    first_name = user_exists['firstName']
    last_name = user_exists['lastName']
    email = user_exists['email']
    selected_room = ObjectId(user_exists['selectedRoom'])
    room = list(mongo.db.chatRooms.find({"_id": selected_room}))[0]
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
    time.sleep(1)
    req = camundarest.complete_external_task(external_task_id, external_task_worker, variables)
    return req

def unos_prijave(external_task_id, external_task_topic, external_task_worker, variables, user):

    user_exists = list(mongo.db.users.find({"username": user}))[0]
    first_name = user_exists['firstName']
    last_name = user_exists['lastName']
    email = user_exists['email']
    selected_room = ObjectId(user_exists['selectedRoom'])
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
    time.sleep(3)
    req = camundarest.complete_external_task(external_task_id, external_task_worker, variables)
    return req 