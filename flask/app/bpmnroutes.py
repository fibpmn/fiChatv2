from app import app
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
import requests
import json
import time
import asyncio
from app import camundarest
from app import xmlparser
from bson import BSON, json_util
from flask_cors import cross_origin
mongo = PyMongo(app)
CORS(app, resources={r'/*': {'origins': '*'}})

#@app.route('/api/<user>/instance/<key>', methods=["GET", "POST"]) change axios
@app.route('/api/instance/<key>', methods=["GET", "POST"])
@cross_origin()
def start_instance(key): #+ parametar user
    #businessKey = str(key) + str(user) ovo radi
    if request.method == "GET":
        return "camundarest.get_process_instances_list(businessKey)"
    else:
        return camundarest.start_process_instance_key(key)

@app.route('/api/task/<assignee>', methods=["GET", "POST"])
@cross_origin()
def get_current_task(assignee):
    if request.method == "GET":
        ass = camundarest.get_task_list(assignee)
        temp = json.loads(ass)
        print(temp[0]['id'])
        return camundarest.get_task_form_variables(temp[0]['id'])
    else:
        return "nesto"

@app.route('/api/task/xml/<key>', methods=["GET"])
@cross_origin()
def get_xml(key):
    if request.method == "GET":
        return xmlparser.something(key)
    else:
        return "nesto"

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
        #Treba povuci usera jer je on prvi assignee na prvom tasku, to usera ukljuciti u poziv start instance u varijablama
        

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

