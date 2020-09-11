from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_cors import cross_origin
from app import camundarest
#for external tasks, mock some services
def test(id, topic, worker):
    variables = {"ToJeTaVariabla": {"value": "Neke male varijable"}}
    pepe = camundarest.fetch_and_lock(worker, topic)
    print("Pepe: ", pepe)
    resp = camundarest.complete_external_task(id, worker, variables)
    print("Resp", )
    return resp

def izracunaj_skolarinu():
    return "ok"

def upisi_studenta():
    return "ok"

def unos_prijave():
    return "ok"