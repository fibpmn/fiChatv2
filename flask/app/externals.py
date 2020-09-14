from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_cors import cross_origin
from app import camundarest
#for external tasks, mock some services
def test(external_task_id, external_task_topic, external_task_worker):
    pepe = camundarest.fetch_and_lock(external_task_worker, external_task_topic)
    print("Pepe: ", pepe)
    variables = {"ToJeTaVariabla": {"value": "Neke male varijable"}}
    resp = camundarest.complete_external_task(external_task_id, external_task_worker, variables)
    print("Resp", )
    return resp

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
    #Pozovi varijable iz baze(chatRooms): Ime, Prezime, status studenta
    #resp = camundarest.complete_external_task(external_task_id, external_task_worker, variables)
    return "ok"

def unos_prijave(external_task_id, external_task_topic, external_task_worker, variables, user):

    #Pozovi varijable iz baze (chatRooms): Ime, Prezime, Mentor,...
    #resp = camundarest.complete_external_task(external_task_id, external_task_worker, variables)
    return "ok"