from app import app
from flask import jsonify
import requests, json, time

url = 'http://localhost:8080/engine-rest'

#EXTERNAL TASK
def get_external_task(processDefinitionId, processInstanceId):
    endpoint = url + '/external-task'
    params = {
        "processDefinitionId": processDefinitionId,
        "processInstanceId": processInstanceId,
    }
    try:
        req = requests.request("GET", endpoint, params=params)
        print(req)
        if req.status_code == 200:
            return req.text
        elif req.status_code == 400:
            return req.text, req.status_code
        elif req.status_code == 500:
            return req.text
    except requests.exceptions.RequestException as error:
        return json.dumps({'Error': str(error)})

def fetch_and_lock(workerId, topicName):
    endpoint = url + "/external-task/fetchAndLock"
    body = {
        "workerId": workerId,
        "maxTasks": 1,
        "asyncResponseTimeout": 5000,
        "topics": [{
            "topicName": topicName,
            "lockDuration": 10000,
        }]
    }
    try:
        req = requests.request("POST", endpoint, json=body)
        if req.status_code == 200:
            return req.text
        elif req.status_code == 500:
            return req.text, req.status_code
    except requests.exceptions.RequestException as error:
        return json.dumps({'Error': str(error)})

def complete_external_task(id, workerId, variables):
    endpoint = url + "/external-task/" + id + "/complete"
    body = {
        "workerId": workerId,
        "variables": variables
    }
    try:
        req = requests.request("POST", endpoint, json=body)
        if req.status_code == 204:
            return req.text
        elif req.status_code == 400:
            return req.text, req.status_code
        elif req.status_code == 404:
            return req.text, req.status_code
        elif req.status_code == 500:
            return req.text, req.status_code
    except requests.exceptions.RequestException as error:
        return json.dumps({'Error': str(error)})

#USER TASK
def get_user_task(processDefinitionId, processInstanceId):
    endpoint = url + '/task'
    params = {
        "processDefinitionId": processDefinitionId,
        "processInstanceId": processInstanceId,
    }
    try:
        req = requests.request("GET", endpoint, params=params)
        print(repr(req))
        if req.status_code == 200:
            return req.text
        elif req.status_code == 400:
            return req.text
        elif req.status_code == 500:
            return req.text
    except requests.exceptions.RequestException as error:
        return json.dumps({'Error': str(error)})

def get_process_xml(id):
    endpoint = url + "/process-definition/" + id + "/xml"
    headers = {"Content-Type": "application/xml"}
    try:
        req = requests.request("GET", endpoint, headers=headers)
        if req.status_code == 200:
            return req.text
        elif req.status_code == 403:
            return req.text, req.status_code
        elif req.status_code == 404:
            return req.text, req.status_code    
    except requests.exceptions.RequestException as error:
        return json.dumps({'Error': str(error)})

def complete_user_task(id, variables):
    endpoint = url + "/task/" + id + "/complete"
    body = {
        "variables": variables,
        "withVariablesInReturn": True
    }
    try:
        req = requests.request("POST", endpoint, json=body)
        if req.status_code == 200:
            return req.text
        elif req.status_code == 204:
            return req.text, req.status_code
        elif req.status_code == 400:
            return req.text, req.status_code
        elif req.status_code == 500:
            return req.text, req.status_code
    except requests.exceptions.RequestException as error:
        return json.dumps({'Error': str(error)})

#PROCESS INSTANCE
def start_process_instance_key(key, user, business_key): #user
    endpoint = url + "/process-definition/key/" + key + "/start"
    body = {
        "variables": {
            "initiator": {
                "value": user,
                "type": "String"
            }
        },
        "businessKey": business_key,
        "withVariablesInReturn": True
    }
    try:
        req = requests.request("POST", endpoint, json=body) 
        if req.status_code == 200:
            return req.text
        elif req.status_code == 400:
            return req.text, req.status_code
        elif req.status_code == 404:
            return req.text, req.status_code
        elif req.status_code == 500:
            return req.text, req.status_code
    except requests.exceptions.RequestException as error:
        return json.dumps({'Error': str(error)})




