from app import app
from flask import jsonify
import requests, json, time

url = 'http://localhost:8080/engine-rest'

#EXTERNAL TASK
def get_external_task(process_definition_id, process_instance_id):
    endpoint = url + '/external-task'
    params = {
        "processDefinitionId": process_definition_id,
        "processInstanceId": process_instance_id,
    }
    try:
        req = requests.request("GET", endpoint, params=params)
        if req.status_code == 200:
            return req.text
        elif req.status_code == 400:
            return req.text, req.status_code
        elif req.status_code == 500:
            return req.text
    except requests.exceptions.RequestException as error:
        return json.dumps({'Error': str(error)})

def fetch_and_lock(worker_id, topic_name):
    endpoint = url + "/external-task/fetchAndLock"
    body = {
        "workerId": worker_id,
        "maxTasks": 1,
        "asyncResponseTimeout": 5000,
        "topics": [{
            "topicName": topic_name,
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

def complete_external_task(task_id, worker_id, variables):
    endpoint = url + "/external-task/" + task_id + "/complete"
    body = {
        "workerId": worker_id,
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
def get_user_task(process_definition_id, process_instance_id):
    endpoint = url + '/task'
    params = {
        "processDefinitionId": process_definition_id,
        "processInstanceId": process_instance_id,
    }
    try:
        req = requests.request("GET", endpoint, params=params)
        if req.status_code == 200:
            return req.text
        elif req.status_code == 400:
            return req.text
        elif req.status_code == 500:
            return req.text
    except requests.exceptions.RequestException as error:
        return json.dumps({'Error': str(error)})

def get_process_xml(process_definition_id):
    endpoint = url + "/process-definition/" + process_definition_id + "/xml"
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

def complete_user_task(task_id, variables):
    endpoint = url + "/task/" + task_id + "/complete"
    print("camundarest.variables: ", variables)
    body = {
        "variables": variables,
        "withVariablesInReturn": True
    }
    try:
        req = requests.request("POST", endpoint, json=body)
        print(req)
        if req.status_code == 200:
            return req.text
        elif req.status_code == 204:
            return req.text
        elif req.status_code == 400:
            return req.text, req.status_code
        elif req.status_code == 500:
            return req.text, req.status_code
    except requests.exceptions.RequestException as error:
        return json.dumps({'Error': str(error)})

#PROCESS INSTANCE
def start_process_instance_key(definition_key, user, business_key): #user
    endpoint = url + "/process-definition/key/" + definition_key + "/start"
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

def check_process_instance_status(process_instance_id, business_key, process_definition_id):
    endpoint = url + "/history/process-instance/"
    params = {
        "processInstanceId": process_instance_id,
        "processInstanceBusinessKey": business_key,
        "processDefinitionId": process_definition_id,
    }
    try:
        req = requests.request("GET", endpoint, params=params)
        if req.status_code == 200:
            return req.text
        elif req.status_code == 404:
            return req.text, req.status_code
        elif req.status_code == 500:
            return req.text, req.status_code
    except requests.exceptions.RequestException as error:
        return json.dumps({'Error': str(error)})

def get_current_task_assignee(process_instance_id, business_key, process_definition_id):
    endpoint = url + "/history/task"
    params = {
        "processInstanceId": process_instance_id,
        "processInstanceBusinessKey": business_key,
        "processDefinitionId": process_definition_id,
        "unfinished": "true"
    }
    try:
        req = requests.request("GET", endpoint, params=params)
        if req.status_code == 200:
            return req.text
        elif req.status_code == 404:
            return req.text, req.status_code
        elif req.status_code == 500:
            return req.text, req.status_code
    except requests.exceptions.RequestException as error:
        return json.dumps({'Error': str(error)})