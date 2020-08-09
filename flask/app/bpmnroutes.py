from app import app
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
import requests
import json
import time
from bson import BSON, json_util

mongo = PyMongo(app)
CORS(app, resources={r'/*': {'origins': '*'}})
#Trebat ce nam jsonify za flask
global engine
engine = True
global url 
url = 'http://localhost:8080/engine-rest' 
global workerId

#napisi funkciju za deployment na bpmn
#daj parametre koji su ti potrebni za topic
#ova funkcija mora nesto vratiti, u vecini slucajeva je json objekt

def get_process_definition(id):
    endpoint = url + "/process-definition/" + str(id)
    response = requests.request("GET", endpoint)
    if(response.status_code == 200):
        data = json.loads(response.text)
        return data
    else:
        error = json.loads(response.text), response.status_code
        return error

def get_process_definition_list(key, status, sortBy, sortOrder):
    endpoint = url + "/process-definition"
    payload = {
        "key": key,
        "active": status,
        "sortBy": sortBy,
        "sortOrder": sortOrder
    }
    response = requests.request("GET", endpoint, params=payload)
    if(response.status_code == 200):
        data = json.loads(response.text)
        return data
    else:
        error = json.loads(response.text), response.status_code
        return error

def delete_process_definition_id(id):
    endpoint = url + "/process-definition/" + id
    payload = {
        "cascade": True
    } 
    response = requests.request("DELETE", endpoint, params=payload)
    if(response.status_code == 200):
        return {"Request successful": response.status_code}
    else:
        error = json.loads(response.text), response.status_code
        return error

def delete_process_definition_key(key):
    endpoint = url + "/process-definition/key/" + key + "/delete"
    payload = {
        "cascade": True
    } 
    response = requests.request("DELETE", endpoint, params=payload)
    if(response.status_code == 204):
        return {"Request successful": response.status_code}
    elif(response.status_code == 403):
        error = json.loads(response.text), response.status_code
        return error
    else:
        error = json.loads(response.text), response.status_code
        return error

def get_deployment(id):
    endpoint = url + "/deployment/" + id
    response = requests.request("GET", endpoint)
    if(response.status_code == 200):
        data = json.loads(response.text)
        return data
    else:
        error = json.loads(response.text), response.status_code
        return error

def get_deployment_list(name, status, sortBy, sortOrder):
    endpoint = url + "/deployment"
    payload = {
        "name": name,
        "active": status,
        "sortBy": sortBy,
        "sortOrder": sortOrder
    }
    response = requests.request("GET", endpoint, params=payload)
    if(response.status_code == 200):
        data = json.loads(response.text)
        return data
    else:
        error = json.loads(response.text), response.status_code
        return error

def process_deploy(name, file):
    endpoint = url + "/deployment/create"
    payload = {
        "deployment-name": name,
    }
    files = {"file": open(file, 'rb')}
    response = requests.request("POST", endpoint, params=payload, files=files)
    if(response.status_code == 200):
        data = json.loads(response.text)
        return data
    else:
        error = json.loads(response.text), response.status_code
        return error

def delete_deployment(id):
    endpoint = url + "/deployment/" + id
    payload = {
        "cascade": True
    }
    response = requests.request("DELETE", endpoint, params=payload)
    if(response.status_code == 204):
        return "Request succesfull"
    else:
        error = json.loads(response.text), response.status_code
        return error

def get_process_instance(id): 
    endpoint = url + '/process-instance/' + id
    payload = {
        "id": id
    }
    response = requests.request("GET", endpoint, params=payload)
    if(response.status_code == 200):
        data = json.loads(response.text)
        return data
    else:
        error = json.loads(response.text), response.status_code
        return error

def get_process_instances_list(processDefinitionKey, active, sortBy, sortOrder):
    endpoint = url + "/process-instance"
    payload = {
        #"processDefinitionId": processDefinitionId,
        "processDefinitionKey": processDefinitionKey,
        #"deploymentId": deploymentId,
        "active": active,
        #"suspended": "true",
        "sortBy": sortBy,
        "sortOrder": sortOrder,
        #"maxResults": maxResults,
    }
    response = requests.request("GET", endpoint, params=payload)
    if(response.status_code == 200):
        data = json.loads(response.text)
        return data
    else:
        error = json.loads(response.text), response.status_code
        return error

def start_process_instance_id(id, businessKey, withVariablesInReturn):
    endpoint = url + "/process-definition/" + id + "/start"
    payload = {
        "id": id,
    }
    body = {
        # "variables": {
        #     "value": value
        #     "type": type #bool, int,...
        # }
        "businessKey": businessKey,
        "withVariablesInReturn": withVariablesInReturn #true
    }
    response = requests.request("POST", endpoint, params=payload, json=body)
    if(response.status_code == 200):
        data1 = json.loads(response.text), response.status_code
        return data1
    elif(response.status_code == 400):
        data1 = json.loads(response.text), response.status_code
        return data1
    elif(response.status_code == 404):
        data1 = json.loads(response.text), response.status_code
        return data1
    else:
        error = json.loads(response.text), response.status_code
        return error

def start_process_instance_key(key, businessKey, withVariablesInReturn):
    endpoint = url + "/process-definition/key/" + key + "/start"
    payload = {
        "key":key
    }
    body = {
        # "variables": {
        #     "value": value
        #     "type": type #bool, int,...
        # }
        #Possible to instantiate with empty body
        "businessKey": businessKey,
        "withVariablesInReturn": withVariablesInReturn #true
    }
    response = requests.request("POST", endpoint, params=payload, json=body)
    if(response.status_code == 200):
        data1 = json.loads(response.text), response.status_code
        return data1
    elif(response.status_code == 400):
        data1 = json.loads(response.text), response.status_code
        return data1
    elif(response.status_code == 404):
        data1 = json.loads(response.text), response.status_code
        return data1
    else:
        error = json.loads(response.text), response.status_code
        return error

def delete_process_instance(id):
    endpoint = url + "/process-instance/" + id
    payload = {
        "id": id
    }
    response = requests.request("DELETE", endpoint, params=payload)
    if(response.status_code == 204):
        return "Request successful"
    else:
        error = json.loads(response.text), response.status_code
        return error

def suspend_process_definition_id(processDefinitionId, includeProcessInstances):
    endpoint = url + "/process-definition/" + processDefinitionId + "/suspended"
    payload = {
        "processDefinition": processDefinitionId,
    }
    body = {
        "suspended": "true",
        "includeProcessInstances": includeProcessInstances
        #"date"
    }
    response = requests.request("PUT", endpoint, params=payload, json=body)
    if(response.status_code == 204):
        return "Request successful"
    else:
        error = json.loads(response.text), response.status_code
        return error

def activate_process_definition_id(processDefinitionId, includeProcessInstances):
    endpoint = url + "/process-definition/" + processDefinitionId + "/suspended"
    payload = {
        "processDefinition": processDefinitionId,
    }
    body = {
        "suspended": "false",
        "includeProcessInstances": includeProcessInstances
        #"date"
    }
    response = requests.request("PUT", endpoint, params=payload, json=body)
    if(response.status_code == 204):
        return "Request successful"
    else:
        error = json.loads(response.text), response.status_code
        return error

def suspend_process_definition_key(processDefinitionKey, includeProcessInstances):
    endpoint = url + "/process-definition/suspended"
    body = {
        "processDefinitionKey": processDefinitionKey,
        "suspended": "true",
        "includeProcessInstances": includeProcessInstances
    }
    print(endpoint)
    print(body)
    response = requests.request("PUT", endpoint, json=body)
    print(response)
    if(response.status_code == 204):
        return "Request successful"
    elif(response.status_code == 400):
        error = json.loads(response.text), response.status_code
        return error
    else:
        error = json.loads(response.text), response.status_code
        return error

def activate_process_definition_key(processDefinitionKey, includeProcessInstances):
    endpoint = url + "/process-definition/suspended"
    body = {
        "processDefinitionKey": processDefinitionKey,
        "suspended": "false",
        "includeProcessInstances": includeProcessInstances
    }
    print(endpoint)
    print(body)
    response = requests.request("PUT", endpoint, json=body)
    print(response)
    if(response.status_code == 204):
        return "Request successful"
    elif(response.status_code == 400):
        error = json.loads(response.text), response.status_code
        return error
    else:
        error = json.loads(response.text), response.status_code
        return error

def update_process_definition_id(id): #used for Za brisanje iz baze
    endpoint = url + "/process-defintion/" + id + "/history-time-to-live"
    payload = {
        "id": id
    }
    response = requests.request("PUT", endpoint, params=payload)
    if(response.status_code == 204):
        return "Request successful"
    elif(response.status_code == 400):
        error = json.loads(response.text), response.status_code
        return error
    else:
        error = json.loads(response.text), response.status_code
        return error

def suspend_process_instance_by_process_definition(id):
    endpoint = url + "/process-instance/" + id + "/suspended"
    payload = {
        "id": id
    }
    body = {
        "suspended": "true"
    }
    response = requests.request("PUT", endpoint, params=payload, json=body)
    if(response.status_code == 204):
        return jsonify("Request successful")
    else:
        error = response.text, response.status_code
        return error

def activate_process_instance_by_process_definition(id):
    endpoint = url + "/process-instance/" + id + "/suspended"
    payload = {
        "id": id
    }
    body = {
        "suspended": "false"
    }
    response = requests.request("PUT", endpoint, params=payload, json=body)
    if(response.status_code == 204):
        return jsonify("Request successful")
    else:
        error = response.text, response.status_code
        return error



def suspend_process_instance_by_process_definition_key(processDefinitionKey):
    endpoint = url + "/process-instance/suspended"
    body = {
        "processDefinitionKey": processDefinitionKey,
        "suspended": "true"
    }
    response = requests.request("PUT", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify("Request successful")
    else:
        error = response.text, response.status_code
        return error

def activate_process_instance_by_process_definition_key(processDefinitionKey):
    endpoint = url + "/process-instance/suspended"
    body = {
        "processDefinitionKey": processDefinitionKey,
        "suspended": "false"
    }
    response = requests.request("PUT", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify("Request successful")
    else:
        error = response.text, response.status_code
        return error

def get_process_instance_variable(id, varName, deserializeValue):
    endpoint = url + "/process-instance/" + id + "/variables/" + varName
    payload = {
        "deserializeValue": deserializeValue
    }
    response = requests.request("GET", endpoint, params=payload)
    if(response.status_code == 200):
        data = json.loads(response.text), response.status_code
        return jsonify(data)
    else:
        error = response.text, response.status_code
        return error

def get_process_instance_variables_list(id, deserializeValue):
    endpoint = url + "/process-instance/" + id + "/variables"
    payload = {
        "deserializeValue": deserializeValue
    }
    response = requests.request("GET", endpoint, params=payload)
    if(response.status_code == 200):
        data = json.loads(response.text), response.status_code
        return jsonify(data)
    else:
        error = response.text, response.status_code
        return error

def get_process_instance_variable_binary(id, varName): #not tested, no binary data for testing
    endpoint = url + "/process-instance/" + id + "/variables/" + varName + "/data"
    response = requests.request("GET", endpoint)
    if(response.status_code == 200):
        data = json.loads(response.text), response.status_code
        return jsonify(data)
    else:
        error = response.text, response.status_code
        return jsonify(error)

# def post_process_instance_variable_binary():
#     endpoint = url + "/process-instance/" + id + "/variables/" + varName + "/data"
#     body = {
#         "valueType": valueType,
#     }
#     files = {
#         "data": {
#             "filename"
#         }
#     }


def update_process_instance_variable(id, varName, value, varType):
    endpoint = url + "/process-instance/" + id + "/variables/" + varName
    body = {
        "value": value,
        "type": varType,
        #"valueInfo": valueInfo 
    }
    response = requests.request("PUT", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify("Request succesful")
    else:
        error = response.text, response.status_code
        return jsonify(error)

def delete_process_instance_variable(id, varName):
    endpoint = url + "/process-instance/" + id + "/variables/" + varName
    response = requests.request("DELETE", endpoint)
    if(response.status_code == 204):
        return jsonify("Request successful")
    else:
        return jsonify("Request unsuccessful")

def get_task(id):
    endpoint = url + "/task/" + id
    response = requests.request("GET", endpoint)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        error = jsonify(response.text, response.status_code)
        return error

# def get_task_list():
#     endpoint = url + "/task"
#     payload = {
#         "processInstanceId": processInstanceId,
#         "processDefinitionName": processDefinitionName,
#         "processDefinitionKey": processDefinitionKey,
#         "assignee": assignee,
#         "assigneeExpression": assigneeExpression,
#         "owner": owner,
#         "candidateGroup": candidateGroup,
#         "candidateUser": candidateUser,
#         "includeAssignedTasks": includeAssignedTasks,
#         "assigned": assigned,
#         "unassigned": unassigned,
#         "name": name,
#         "createdOn": createdOn, #datum je fckdup  yyyy-MM-dd'T'HH:mm:ss.SSSZ
#         "candidateGroups": candidateGroups,
#         "active": active,
#         "suspended": suspended,
#         "sortBy": sortBy, #id, name
#         "sortOrder": sortOrder, #asc or desc
#         "maxResults": maxResults #int
#     }
#     response = requests.request("GET", endpoint, params=payload)
#     if(response.status_code == 200):
#         return jsonify(response.text, response.status_code)
#     else:
#         error = jsonify(response.text, response.status_code)
#         return error

def claim_task(id, userId):
    endpoint = url + "/task/" + id + "/claim"
    body = {
        "userId": userId
    }
    response = requests.request("POST", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify("Request successful", response.status_code)
    else:
        error = jsonify(response.text, response.status_code)
        return error

def unclaim_task(id):
    endpoint = url + "/task/" + id + "/unclaim"
    response = requests.request("POST", endpoint)
    if(response.status_code == 204):
        return jsonify("Request successful", response.status_code)
    else:
        error = jsonify(response.text, response.status_code)
        return error

def set_asignee(id, userId):
    endpoint = url + "/task/" + id + "/assignee"
    body = {
        "userId": userId
    }
    response = requests.request("POST", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify("Request successful", response.status_code)
    else:
        error = jsonify(response.text, response.status_code)
        return error


# def complete_task(id):                                Mozda rijesiti vanjskom formom, ja se iskreno nadam
#     endpoint = url + "/task/" + id + "/complete"
#     body = {
#         "variables": {
#             "naslov": {"value": "Naslov", "type": "String"},
#             "sazetak": {"value": "Sazetak", "type": "String"},
#             "mentori": [{"value": "Nikola Tankovic", "type": "String"},    
#                        {"value": "Darko Etinger", "type": "String"},
#                        {"value": "Sinisa Milicic", "type": "String"},
#             ]
#         }
#     }
#             # "mentori": {"value": ["Nikola Tankovic", "Darko Etinger", "Sinisa Milicic"], 
#             #              "type": "Object", 
#             #              "valueInfo": {
#             #                   "objectTypeName": "JSON",
#             #                   "serializationDataFormat": "JSON"
#             #             }},

#     response = requests.request("POST", endpoint, json=body)
#     if(response.status_code == 204):
#         return jsonify("Request successful", response.status_code)
#     elif(response.status_code == 400):
#         return jsonify(response.text, response.status_code)
#     else:
#         error = jsonify(response.text, response.status_code)
#         return error

def get_task_formkey(id): # fali path za spajanje forme
    endpoint = url + "/task/" + id + "/form"
    response = requests.request("GET", endpoint)
    if(response.status_code == 200):
        return jsonify(response.text)
    else:
        return jsonify(response.text, response.status_code)

def get_deployed_form(id):
    endpoint = url + "/task/" + id + "/deployed-form"
    response = requests.request("GET", endpoint)
    if(response.status_code == 200):
        return jsonify(response.text)
    elif(response.status_code == 400):
        return jsonify(response.text, response.status_code)
    elif(response.status_code == 403):
        return jsonify(response.text, response.status_code)    
    else:
        return jsonify(response.text, response.status_code)

def submit_form(id, variables): #nedovrseno
    endpoint = url + "/task/" + id + "/submit-form"
    body = {
        "variables": variables
    }
    response = requests.request("POST", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify(response.text)
    elif(response.status_code == 400):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_task_form_variables(id, deserializeValues): 
    endpoint = url + "/task/" + id + "/form-variables"
    payload = {
        #"variableNames": variableNames, #moze i bez toga, struktura podataka je lista  variableNames,
        "deserializeValues": deserializeValues
    }
    response = requests.request("GET", endpoint, params=payload)
    if(response.status_code == 200):
        return jsonify(response.text)
    else:
        return jsonify(response.text, response.status_code)

def get_task_variable(id, varName, deserializeValue):
    endpoint = url + "/task/" + id + "/variables/" + varName
    payload = {
        "deserializeValue": deserializeValue
    }
    response = requests.request("GET", endpoint, json=payload)
    if(response.status_code == 200):
        return jsonify(response.text)
    elif(response.status_code == 404):
        return jsonify(response.text, response.status_code)  
    else:
        return jsonify(response.text, response.status_code)    

def get_task_variables(id, deserializeValues):
    endpoint = url + "/task/" + id + "/variables"
    payload = {
        "deserializeValues": deserializeValues
    }
    response = requests.request("GET", endpoint, params=payload)
    if(response.status_code == 200):
        return jsonify(response.text)
    else:
        return jsonify(response.text, response.status_code)


###### TESTIRANJE
@app.route("/api", methods=["GET", "POST", "DELETE", "PUT"])

# def nesto31():
#     calls = complete_task("f6ea7551-da54-11ea-8fe7-60f262e99a90")
#     return calls
# def nesto32():
#     calls = get_task_formkey("8d36fe1f-da58-11ea-8fe7-60f262e99a90")
#     return calls
# def nesto33():
#     calls = get_deployed_form("8d36fe1f-da58-11ea-8fe7-60f262e99a90")
#     return calls
# def nesto34():
#    calls = submit_form("id", "varijable")
#    return calls
# def nesto35():
#     calls = get_task_form_variables("f7b7f6ba-da62-11ea-8fe7-60f262e99a90", True)
#     return calls
# def nesto36():
#     calls = set_asignee("f7b7f6ba-da62-11ea-8fe7-60f262e99a90", "ToniID")
#     return calls
# def nesto37():
#     calls = get_task_variable("7aa6d274-d99c-11ea-b794-60f262e99a90", "Odgovor", True)
#     return calls
def nesto38():
    calls = get_task_variables("7aa6d274-d99c-11ea-b794-60f262e99a90", True)
    return calls

#get task variables list 
#get task variable binary
#post task variable binary
#delete task variable binary
#update task variable


#get external task
#get external task list
#fetch and lock
#complete external task
#handle external task error




# def nesto():
#     call = get_process_definition("Process_1qz246f:1:cb9690c3-d727-11ea-ac56-60f262e99a90")
#     return jsonify(call)
# def nesto1():
#     call = get_process_definition_list("Process_1qz246f", "true", "key", "desc") #tuple
#     data = jsonify(call)
#     return data
# def nesto2():
#     call = delete_process_definition_id("Process_1qz246f:1:cb9690c3-d727-11ea-ac56-60f262e99a90")
#     return call
# def nesto3():
#     call = delete_process_definition_key("PrijavaZavrsnog")
#     return call
# def nesto4():
#     call = get_deployment("14a733dd-c9bf-11ea-ae47-60f262e99a90")
#     return call
# def nesto5():
#     calls = get_deployment_list("diagram_1", "true", "name", "desc") #tuple
#     data = jsonify(calls)
#     return data
# def nesto6():
#     calls = process_deploy("PrijavaRada","C:/Users/Dell/Documents/Fakultet/Završnirad/dijagrami/PrijavaZavrsnogRada.bpmn")
#     print(calls)
#     return calls
# def nesto7():
#     calls = delete_deployment("692a21fd-d963-11ea-b794-60f262e99a90")
#     return calls
# def nesto8():
#     calls = get_process_instance("f1c5124f-d965-11ea-b794-60f262e99a90")
#     return calls
# def nesto9():
#     calls = get_process_instances_list("PrijavaZavrsnog","true","definitionKey","desc")
#     data = jsonify(calls)
#     return data
# def nesto10():
#     calls = start_process_instance_id("PrijavaZavrsnog:1:cda0726e-d965-11ea-b794-60f262e99a90", 1, "true")
#     return calls
# def nesto11():
#     calls = start_process_instance_key("PrijavaZavrsnog", 1, "true")
#     return calls
# def nesto12():
#     calls = delete_process_instance("f1c5124f-d965-11ea-b794-60f262e99a90")
#     return calls
# def nesto13():
#     calls = suspend_process_definition_id("PrijavaZavrsnog:1:cda0726e-d965-11ea-b794-60f262e99a90", "true")#, update_process_definition_id("PrijavaZavrsnog:1:cda0726e-d965-11ea-b794-60f262e99a90")
#     return jsonify(calls)
# def nesto14():
#     calls = activate_process_definition_id("PrijavaZavrsnog:1:cda0726e-d965-11ea-b794-60f262e99a90", "true")
#     return jsonify(calls)
# def nesto15():
#     calls = suspend_process_definition_key("PrijavaZavrsnog", "true")
#     return jsonify(calls)
# def nesto16():
#     calls = activate_process_definition_key("PrijavaZavrsnog", "true")
#     return jsonify(calls)
# def nesto17():
#     calls = update_process_definition_id("PrijavaZavrsnog:1:cda0726e-d965-11ea-b794-60f262e99a90")
#     return jsonify(calls)
# def nesto18():
#     calls = suspend_process_instance_by_process_definition("PrijavaZavrsnog:1:cda0726e-d965-11ea-b794-60f262e99a90")
#     return calls
# def nesto19():
#     calls = activate_process_instance_by_process_definition("PrijavaZavrsnog:1:cda0726e-d965-11ea-b794-60f262e99a90")
#     return calls
# def nesto20():
#     calls = suspend_process_instance_by_process_definition_key("PrijavaZavrsnog")
#     return calls
# def nesto21():
#     calls = activate_process_instance_by_process_definition_key("PrijavaZavrsnog")
#     return calls
# def nesto22():
#     calls = get_process_instance_variable("f6325786-d965-11ea-b794-60f262e99a90", "Naslov", True)
#     return calls
# def nesto23():
#     calls = get_process_instance_variables_list("f6325786-d965-11ea-b794-60f262e99a90", True)
#     return calls
# def nesto24():
#     calls = get_process_instance_variable_binary("f6325786-d965-11ea-b794-60f262e99a90", "PotencijalniMentori")
#     return calls
# def nesto25():
#     calls = update_process_instance_variable("f6325786-d965-11ea-b794-60f262e99a90", "Naslov", "Pepe Pepito", "String")
#     return calls
# def nesto26():
#     calls = delete_process_instance_variable("f6325786-d965-11ea-b794-60f262e99a90", "Sazetak")
#     return calls
# def nesto27():
#     calls = get_task("7aa6d274-d99c-11ea-b794-60f262e99a90")
#     return calls
# def nesto28(): #not tested
#     calls = get_task_list("milijarda parametara")
#     return calls
# def nesto29():
#     calls = claim_task("7aa6d274-d99c-11ea-b794-60f262e99a90","ToniID")
#     return calls
# def nesto30():
#     calls = unclaim_task("7aa6d274-d99c-11ea-b794-60f262e99a90")
#     return calls




















def fetch_and_lock(self, topic, lockDuration=1000):
    endpoint = str(self.url) + 'external-task/fetchAndLock'
    workerId = str(self.workerId)
    payload = {
        "workerId": workerId,
        "maxTasks": 1,
        "topics": [{
            "topicName": topic,
            "lockDuration": lockDuration
            #variables -> JSON array, if not included, all variables will be fetched
            #"variables": [orderId]
            #deserializeValues: true || false 
        }]
    }
    try:
        response = requests.request("POST", endpoint, json=payload)
        if response.status_code == 200: print('OK') 
        print(response.status_code)
        body = response.text
    except:
        engine = False
        if response.status_code == 500: print('Internal Server Error')
        print('Engine is down')
        if engine == True:
            while body != '[]':
                print('Polling')
                fetch_and_lock = requests.request("POST", endpoint, json=payload)
                time.sleep(5)
                if body != '[]': break

def extend_lock(self, taskid, workerId):
    taskid = str(taskid)
    endpoint = str(self.url) + '/external-task' + taskid + '/extendLock'
    workerId = str(self.workerId)
    payload = {
        "newDuration": 5000,
        "workerId": workerId
    }
    try:
        response = requests.request("POST", endpoint, json=payload)
        if response.status_code == 204: print('No Content')
    except:
        if response.status_code == 400: 
            print('Bad Request')
        elif response.status_code == 404: 
            print('Not Found')



# def externalTask(taskid):
#     pepe = external("http://localhost:8080/engine-rest", "1")
#     taskid = "cbf356c8-d727-11ea-ac56-60f262e99a90"
#     pepe.get_external_task(taskid)
#     return jsonify(pepe)
    # return pepe.get_external_task(taskid)