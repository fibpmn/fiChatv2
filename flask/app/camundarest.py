from app import app
from flask import jsonify
import requests, json, time

global url 
url = 'http://localhost:8080/engine-rest' 

#make handle_response_codes function


def get_user_task_form(processDefinitionId, user):
    endpoint = url + '/task'
    params = {
        "processDefinitionId": processDefinitionId,
        "assignee": user,
        "assigned": "true",
        "active": "true"
    }
    response = requests.request("GET", endpoint, params=params)
    if(response.status_code == 200):
        return response.text
    else: 
        return response.text, response.status_code

def get_process_definition(id):
    endpoint = url + "/process-definition/" + id
    response = requests.request("GET", endpoint)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_process_definition_list(key, status, sortBy, sortOrder):
    endpoint = url + "/process-definition"
    params = {
        "key": key,
        "active": status,
        "sortBy": sortBy,
        "sortOrder": sortOrder
    }
    response = requests.request("GET", endpoint, params=params)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_process_instance(id): 
    endpoint = url + '/process-instance/' + id
    response = requests.request("GET", endpoint)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_process_instances_list(businessKey):
    endpoint = url + "/process-instance"
    params = {
        #"processDefinitionId": processDefinitionId, processDefinitionId
        #"processDefinitionKey": processDefinitionKey,  processDefinitionKey, 
        "businessKey": businessKey,  
        #"deploymentId": deploymentId,
        #"active": active, , active,
        #"suspended": "true",
        #"sortBy": sortBy, sortBy, sortOrder
        #"sortOrder": sortOrder,
        #"maxResults": maxResults,
    }
    response = requests.request("GET", endpoint, params=params)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def start_process_instance_id(id, businessKey, withVariablesInReturn):
    endpoint = url + "/process-definition/" + id + "/start"
    body = {
        # "variables": {
        #     "value": value
        #     "type": type #bool, int,...
        # }
        "businessKey": businessKey,
        "withVariablesInReturn": withVariablesInReturn #true
    }
    response = requests.request("POST", endpoint, json=body)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    elif(response.status_code == 400):
        return jsonify(response.text, response.status_code)
    elif(response.status_code == 404):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def start_process_instance_key(key, user): #user
    endpoint = url + "/process-definition/key/" + key + "/start"
    businessKey = str(key) + str(user)
    body = {
        "variables": {
            "initiator": {
                "value": user,
                "type": "String"
            }
        },
        "businessKey": businessKey,
        "withVariablesInReturn": True
    }
    response = requests.request("POST", endpoint, json=body)
    if(response.status_code == 200):
        return response.text
    elif(response.status_code == 400):
        return jsonify(response.text, response.status_code)
    elif(response.status_code == 404):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def delete_process_instance(id):
    endpoint = url + "/process-instance/" + id
    response = requests.request("DELETE", endpoint)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_process_instance_variable(id, varName, deserializeValue):
    endpoint = url + "/process-instance/" + id + "/variables/" + varName
    payload = {
        "deserializeValue": deserializeValue
    }
    response = requests.request("GET", endpoint, params=payload)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_process_instance_variables_list(id):
    endpoint = url + "/process-instance/" + id + "/variables"
    params = {
        "deserializeValue": True
    }
    response = requests.request("GET", endpoint, params=params)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_task(id):
    endpoint = url + "/task/" + id
    response = requests.request("GET", endpoint)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_task_list(assignee):
    endpoint = url + "/task"
    params = {
        # "processInstanceId": processInstanceId,
        # "processDefinitionName": processDefinitionName,
        # "processDefinitionKey": processDefinitionKey,
        "assignee": assignee,
        # "assigneeExpression": assigneeExpression,
        # "owner": owner,
        # "candidateGroup": candidateGroup,
        # "candidateUser": candidateUser,
        # "includeAssignedTasks": includeAssignedTasks,
        # "assigned": assigned,
        # "unassigned": unassigned,
        # "name": name,
        # "createdOn": createdOn, #datum je fckdup  yyyy-MM-dd'T'HH:mm:ss.SSSZ
        # "candidateGroups": candidateGroups,
        # "active": active,
        # "suspended": suspended,
        # "sortBy": sortBy, #id, name
        # "sortOrder": sortOrder, #asc or desc
        # "maxResults": maxResults #int
    }
    response = requests.request("GET", endpoint, params=params)
    if(response.status_code == 200):
        return response.text
    else:
        error = jsonify(response.text, response.status_code)
        return error

def set_assignee(id, userId):
    endpoint = url + "/task/" + id + "/assignee"
    body = {
        "userId": userId
    }
    response = requests.request("POST", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_task_form_variables(id): 
    endpoint = url + "/task/" + id + "/form-variables"
    params = {
        #"variableNames": variableNames, #moze i bez toga, struktura podataka je lista  variableNames,
        "deserializeValues": "false"
    }
    response = requests.request("GET", endpoint, params=params)
    if(response.status_code == 200):
        return response.text
    else:
        return jsonify(response.text, response.status_code)

def get_task_variable(id, varName, deserializeValue):
    endpoint = url + "/task/" + id + "/variables/" + varName
    params = {
        "deserializeValue": deserializeValue
    }
    response = requests.request("GET", endpoint, json=params)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    elif(response.status_code == 404):
        return jsonify(response.text, response.status_code)  
    else:
        return jsonify(response.text, response.status_code)    

def get_task_variables(id, deserializeValues):
    endpoint = url + "/task/" + id + "/variables"
    params = {
        "deserializeValues": deserializeValues
    }
    response = requests.request("GET", endpoint, params=params)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def update_task_variable(id, varName, Value, Type):
    endpoint = url + "/task/" + id + "/variables/" + varName
    body = {
        "value": Value,
        "type": Type,
    }
    response = requests.request("PUT", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    elif(response.status_code == 400):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_external_task(id):
    endpoint = url + "/external-task/" + id
    response = requests.request("GET", endpoint)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_external_tasks(topicName):
    endpoint = url + "/external-task/"
    params = {
        "topicName": topicName
    }
    response = requests.request("GET", endpoint, params=params)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def fetch_and_lock(workerId, maxTasks, topicName):
    endpoint = url + "/external-task/fetchAndLock"
    body = {
        "workerId": workerId,
        "maxTasks": maxTasks,
        "topics": [{
            "topicName": topicName,
            "lockDuration": 10000,
            # "variables:" [{
            #     "value": Value,
            #     "type": Type
            # }]
        }]
    }
    response = requests.request("POST", endpoint, json=body)
    print(response.text)
    if(response.status_code == 200):
        return response.text
    else:
        return jsonify(response.text, response.status_code)

def complete_external_task(id, workerId, mentori):
    endpoint = url + "/external-task/" + id + "/complete"
    body = {
        "workerId": workerId,
        "variables": {
            "Mentori": { 
                "value": mentori     
            }
        }
    }
    response = requests.request("POST", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    elif(response.status_code == 400):
        return jsonify(response.text, response.status_code)    
    elif(response.status_code == 404):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_process_xml(id):
    endpoint = url + "/process-definition/" + id + "/xml"
    headers = {"Content-Type": "application/xml"}
    response = requests.request("GET", endpoint, headers=headers) 
    if(response.status_code == 200):
        return json.loads(response.text)
    elif(response.status_code == 403):
        return response.text, response.status_code
    else:
        return response.text, response.status_code

def complete_task(id, vars):
    endpoint = url + "/task/" + id + "/complete"
    #print("PRIJE camundarest: ", vars)
    body = {
        "variables": vars,
        "withVariablesInReturn": True
    }
    #print("POSLIJE camundarest: ", vars)
    response = requests.request("POST", endpoint, json=body)
    if(response.status_code == 200):
        return response.text
    else:
        error = jsonify(response.text, response.status_code)
        return error

def submit_task_form(id, vars):
    endpoint = url + "/task/" + id + "/submit-form"
    body = {
        "variables": vars,
        "withVariablesInReturn": True
    }
    print("camundarest: ", vars)
    response = requests.request("POST", endpoint, json=body)
    if(response.status_code == 200):
        return response.text
    else:
        error = jsonify(response.text, response.status_code)
        return error



# def delete_process_definition_id(id):
#     endpoint = url + "/process-definition/" + id
#     params = {
#         "cascade": True
#     } 
#     response = requests.request("DELETE", endpoint, params=params)
#     if(response.status_code == 200):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def delete_process_definition_key(key):
#     endpoint = url + "/process-definition/key/" + key + "/delete"
#     params = {
#         "cascade": True
#     } 
#     response = requests.request("DELETE", endpoint, params=params)
#     if(response.status_code == 204):
#         return jsonify(response.text, response.status_code)
#     elif(response.status_code == 403):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def get_deployment(id):
#     endpoint = url + "/deployment/" + id
#     response = requests.request("GET", endpoint)
#     if(response.status_code == 200):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def get_deployment_list(name, status, sortBy, sortOrder):
#     endpoint = url + "/deployment"
#     params = {
#         "name": name,
#         "active": status,
#         "sortBy": sortBy,
#         "sortOrder": sortOrder
#     }
#     response = requests.request("GET", endpoint, params=params)
#     if(response.status_code == 200):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def process_deploy(name, file):
#     endpoint = url + "/deployment/create"
#     params = {
#         "deployment-name": name,
#     }
#     files = {"file": open(file, 'rb')}
#     response = requests.request("POST", endpoint, params=params, files=files)
#     if(response.status_code == 200):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def delete_deployment(id):
#     endpoint = url + "/deployment/" + id
#     params = {
#         "cascade": True
#     }
#     response = requests.request("DELETE", endpoint, params=params)
#     if(response.status_code == 204):
#         return "Request succesfull"
#     else:
#         error = json.loads(response.text), response.status_code
#         return error

# def get_activity_tree(id):
#     endpoint = url + "/process-instance/" + id + "/activity-instances"
#     response = requests.request("GET", endpoint) 
#     res = isinstance(response.text, str)
#     print(res)
#     temp = json.loads(response.text)
#     #temp['childActivityInstances'][0]["childActivityInstances"][2]["id"]
#     subprocess_id = temp['childActivityInstances'][0]["childActivityInstances"]
#     for i in range(len(subprocess_id)):
#         print(subprocess_id[i]["id"])
#         print(subprocess_id[i]["activityId"])
#         print(subprocess_id[i]["activityType"])
#         print(subprocess_id[i]["activityName"])
#     if(response.status_code == 200):
#         return response.text
#         #jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def get_subprocesses(processInstanceId):
#     endpoint = url + "/history/activity-instance"
#     params = {
#         #"superProcessInstanceId": superProcessInstanceIdsuperProcessInstanceId process-instance
#         #"activityType": activityType, , activityType
#         #"activityId": activityId, activityId
#         #"businessKey": "nada"
#         "processInstanceId": processInstanceId,
#     }
#     response = requests.request("GET", endpoint, params=params)
#     if(response.status_code == 200):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def suspend_process_definition_id(processDefinitionId, includeProcessInstances):
#     endpoint = url + "/process-definition/" + processDefinitionId + "/suspended"
#     params = {
#         "processDefinition": processDefinitionId,
#     }
#     body = {
#         "suspended": "true",
#         "includeProcessInstances": includeProcessInstances
#         #"date"
#     }
#     response = requests.request("PUT", endpoint, params=params, json=body)
#     if(response.status_code == 204):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def activate_process_definition_id(processDefinitionId, includeProcessInstances):
#     endpoint = url + "/process-definition/" + processDefinitionId + "/suspended"
#     params = {
#         "processDefinition": processDefinitionId,
#     }
#     body = {
#         "suspended": "false",
#         "includeProcessInstances": includeProcessInstances
#         #"date"
#     }
#     response = requests.request("PUT", endpoint, params=params, json=body)
#     if(response.status_code == 204):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def suspend_process_definition_key(processDefinitionKey, includeProcessInstances):
#     endpoint = url + "/process-definition/suspended"
#     body = {
#         "processDefinitionKey": processDefinitionKey,
#         "suspended": "true",
#         "includeProcessInstances": includeProcessInstances
#     }
#     response = requests.request("PUT", endpoint, json=body)
#     if(response.status_code == 204):
#         return jsonify(response.text, response.status_code)
#     elif(response.status_code == 400):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def activate_process_definition_key(processDefinitionKey, includeProcessInstances):
#     endpoint = url + "/process-definition/suspended"
#     body = {
#         "processDefinitionKey": processDefinitionKey,
#         "suspended": "false",
#         "includeProcessInstances": includeProcessInstances
#     }
#     response = requests.request("PUT", endpoint, json=body)
#     if(response.status_code == 204):
#         return jsonify(response.text, response.status_code)
#     elif(response.status_code == 400):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def update_process_definition_id(id): #used for Za brisanje iz baze
#     endpoint = url + "/process-defintion/" + id + "/history-time-to-live"
#     response = requests.request("PUT", endpoint)
#     if(response.status_code == 204):
#         return jsonify(response.text, response.status_code)
#     elif(response.status_code == 400):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def suspend_process_instance_by_process_definition(id):
#     endpoint = url + "/process-instance/" + id + "/suspended"
#     body = {
#         "suspended": "true"
#     }
#     response = requests.request("PUT", endpoint, json=body)
#     if(response.status_code == 204):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def activate_process_instance_by_process_definition(id):
#     endpoint = url + "/process-instance/" + id + "/suspended"
#     body = {
#         "suspended": "false"
#     }
#     response = requests.request("PUT", endpoint, json=body)
#     if(response.status_code == 204):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def suspend_process_instance_by_process_definition_key(processDefinitionKey):
#     endpoint = url + "/process-instance/suspended"
#     body = {
#         "processDefinitionKey": processDefinitionKey,
#         "suspended": "true"
#     }
#     response = requests.request("PUT", endpoint, json=body)
#     if(response.status_code == 204):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def activate_process_instance_by_process_definition_key(processDefinitionKey):
#     endpoint = url + "/process-instance/suspended"
#     body = {
#         "processDefinitionKey": processDefinitionKey,
#         "suspended": "false"
#     }
#     response = requests.request("PUT", endpoint, json=body)
#     if(response.status_code == 204):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def get_process_instance_variable_binary(id, varName): #not tested, no binary data for testing
#     endpoint = url + "/process-instance/" + id + "/variables/" + varName + "/data"
#     response = requests.request("GET", endpoint)
#     if(response.status_code == 200):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def update_process_instance_variable(id, varName, value, varType):
#     endpoint = url + "/process-instance/" + id + "/variables/" + varName
#     body = {
#         "value": value,
#         "type": varType,
#         #"valueInfo": valueInfo 
#     }
#     response = requests.request("PUT", endpoint, json=body)
#     if(response.status_code == 204):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def delete_process_instance_variable(id, varName):
#     endpoint = url + "/process-instance/" + id + "/variables/" + varName
#     response = requests.request("DELETE", endpoint)
#     if(response.status_code == 204):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def claim_task(id, userId):
#     endpoint = url + "/task/" + id + "/claim"
#     body = {
#         "userId": userId
#     }
#     response = requests.request("POST", endpoint, json=body)
#     if(response.status_code == 204):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def unclaim_task(id):
#     endpoint = url + "/task/" + id + "/unclaim"
#     response = requests.request("POST", endpoint)
#     if(response.status_code == 204):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)


# def get_task_formkey(id): # fali path za spajanje forme
#     endpoint = url + "/task/" + id + "/form"
#     response = requests.request("GET", endpoint)
#     if(response.status_code == 200):
#         return jsonify(response.text, response.status_code)
#     else:
#         return jsonify(response.text, response.status_code)

# def get_deployed_form(id):
#     endpoint = url + "/task/" + id + "/deployed-form"
#     response = requests.request("GET", endpoint)
#     if(response.status_code == 200):
#         return jsonify(response.text, response.status_code)
#     elif(response.status_code == 400):
#         return jsonify(response.text, response.status_code)
#     elif(response.status_code == 403):
#         return jsonify(response.text, response.status_code)    
#     else:
#         return jsonify(response.text, response.status_code)


###### TESTIRANJE
#@app.route("/api", methods=["GET", "POST", "DELETE", "PUT"])
#def funkcija():
