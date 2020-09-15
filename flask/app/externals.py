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
def izracunaj_skolarinu(external_task_id, external_task_topic, external_task_worker, variables):
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
    resp = camundarest.complete_external_task(external_task_id, external_task_worker, variables)        
    return resp

def upisi_studenta(external_task_id, external_task_topic, external_task_worker, variables, user):
    user_exists = list(mongo.db.users.find({"username": user}))
    print(upisi_studenta)
    #Pozovi varijable iz baze(chatRooms): Ime, Prezime, status studenta
    #resp = camundarest.complete_external_task(external_task_id, external_task_worker, variables)
    return "ok"

def unos_prijave(external_task_id, external_task_topic, external_task_worker, variables, user):
    user_exists = list(mongo.db.users.find({"username": user}))[0]
    first_name = user_exists['firstName']
    last_name = user_exists['lastName']
    email = user_exists['email']
    selected_room = ObjectId(user_exists['selectedRoom'])
    room = list(mongo.db.chatRooms.find({"_id": selected_room}))[0]
    print("Zapravo je Room: ", room)
    for room_variables in room['variables']:
        variables = room_variables
    data = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "variables": variables
    }
    mongo.db.submitedApplications.insert_one(data)
    camundarest.fetch_and_lock(external_task_worker, external_task_topic)
    req = camundarest.complete_external_task(external_task_id, external_task_worker, variables)
    return req #"Čestitamo! Uspješno ste prijavili završni rad"