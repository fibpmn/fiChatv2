from app import app
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
import requests
import json
import time
from app import camundarest
from bson import BSON, json_util
from flask_cors import cross_origin
mongo = PyMongo(app)
CORS(app, resources={r'/*': {'origins': '*'}})

# def start_process_instance_id(id, businessKey, withVariablesInReturn):
#     endpoint = url + "/process-definition/" + id + "/start"
#     body = {
#         # "variables": {
#         #     "value": value
#         #     "type": type #bool, int,...
#         # }
#         "businessKey": businessKey,
#         "withVariablesInReturn": withVariablesInReturn #true
#     }
#     response = requests.request("POST", endpoint, json=body)
#     if(response.status_code == 200):
#         return jsonify(response.text, response.status_code)
#     elif(response.status_code == 400):
#         return jsonify(response.text, response.status_code)
#     elif(response.status_code == 404):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

#@app.route('/api/')

@app.route('/api/send')
@cross_origin()
def first_user_task():
    content = request.get_json()
    temp = json.dumps(content) #content je sada string
    print(temp)
    temp1 = json.loads(temp)
    naslov = temp1['naslov']
    sazetak = temp1['sazetak']
    mentori_1 = temp1['mentori'][0]['value']
    mentori_2 = temp1['mentori'][1]['value']
    # variables = {
    #     "Naslov": naslov,
    #     "Sazetak": sazetak,
    #     "Mentori": 
    # }
    if request.method == 'POST':
        camundarest.start_process_instance_key("PrijavaZavrsnogRada", "somethingNew", True)
        print(naslov)
        print(sazetak)
        print(mentori_1)
        print(mentori_2)
        return "PEPE"
    else:
        varijable = request.get_json()
        return varijable
        #Treba povuci usera jer je on prvi assignee na prvom tasku, to usera ukljuciti u poziv start instance u varijablama
        

@app.route('/api/start-instance', methods=['POST', 'GET'])
@cross_origin()
def start_instance():
    if request.method == 'POST':
        camundarest.start_process_instance_key("PrijavaZavrsnogRada", "", False)
        print("Something")
        return "yas"   
    else:
        return "Pepe"
    # print(varijable)
    # return varijable 

