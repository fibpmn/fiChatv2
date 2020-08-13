from app import app
from flask import jsonify
import requests, json, time


global url 
url = 'http://localhost:8080/engine-rest' 

#make handle_response_codes function

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

def delete_process_definition_id(id):
    endpoint = url + "/process-definition/" + id
    params = {
        "cascade": True
    } 
    response = requests.request("DELETE", endpoint, params=params)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def delete_process_definition_key(key):
    endpoint = url + "/process-definition/key/" + key + "/delete"
    params = {
        "cascade": True
    } 
    response = requests.request("DELETE", endpoint, params=params)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    elif(response.status_code == 403):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_deployment(id):
    endpoint = url + "/deployment/" + id
    response = requests.request("GET", endpoint)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_deployment_list(name, status, sortBy, sortOrder):
    endpoint = url + "/deployment"
    params = {
        "name": name,
        "active": status,
        "sortBy": sortBy,
        "sortOrder": sortOrder
    }
    response = requests.request("GET", endpoint, params=params)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def process_deploy(name, file):
    endpoint = url + "/deployment/create"
    params = {
        "deployment-name": name,
    }
    files = {"file": open(file, 'rb')}
    response = requests.request("POST", endpoint, params=params, files=files)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def delete_deployment(id):
    endpoint = url + "/deployment/" + id
    params = {
        "cascade": True
    }
    response = requests.request("DELETE", endpoint, params=params)
    if(response.status_code == 204):
        return "Request succesfull"
    else:
        error = json.loads(response.text), response.status_code
        return error

def get_process_instance(id): 
    endpoint = url + '/process-instance/' + id
    response = requests.request("GET", endpoint)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_activity_tree(id):
    endpoint = url + "/process-instance/" + id + "/activity-instances"
    response = requests.request("GET", endpoint) 
    res = isinstance(response.text, str)
    print(res)
    temp = json.loads(response.text)
    #temp['childActivityInstances'][0]["childActivityInstances"][2]["id"]
    subprocess_id = temp['childActivityInstances'][0]["childActivityInstances"]
    for i in range(len(subprocess_id)):
        print(subprocess_id[i]["id"])
        print(subprocess_id[i]["activityId"])
        print(subprocess_id[i]["activityType"])
        print(subprocess_id[i]["activityName"])
    if(response.status_code == 200):
        return response.text
        #jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)


def get_subprocesses(processInstanceId):
    endpoint = url + "/history/activity-instance"
    params = {
        #"superProcessInstanceId": superProcessInstanceIdsuperProcessInstanceId process-instance
        #"activityType": activityType, , activityType
        #"activityId": activityId, activityId
        #"businessKey": "nada"
        "processInstanceId": processInstanceId,
    }
    response = requests.request("GET", endpoint, params=params)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)



def get_process_instances_list( caseInstanceId):
    endpoint = url + "/process-instance"
    params = {
        #"processDefinitionId": processDefinitionId, processDefinitionId
        #"processDefinitionKey": processDefinitionKey,  processDefinitionKey, 
        #"businessKey": businessKey,  businessKey
        #"caseInstanceId":caseInstanceId,
        #"superProcessInstance": superProcessInstance, superProcessInstance,
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

def start_process_instance_key(key, businessKey, withVariablesInReturn):
    endpoint = url + "/process-definition/key/" + key + "/start"
    variables = {
             "name": "varName", 
             "value": "ToniID",
             "type": "String" 
            }
    #data = json.dumps(variables)
    #res = isinstance(data, str)
    #print(res)
    body = {
        "variables": {
            "varName": {
                "value": "ToniID",
                "type": "String"
            }
        },
        "businessKey": businessKey,
        "withVariablesInReturn": withVariablesInReturn #true
    }
    response = requests.request("POST", endpoint, json=body)
    if(response.status_code == 200):
        print(response.text)
        return jsonify(response.text, response.status_code)
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

def suspend_process_definition_id(processDefinitionId, includeProcessInstances):
    endpoint = url + "/process-definition/" + processDefinitionId + "/suspended"
    params = {
        "processDefinition": processDefinitionId,
    }
    body = {
        "suspended": "true",
        "includeProcessInstances": includeProcessInstances
        #"date"
    }
    response = requests.request("PUT", endpoint, params=params, json=body)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def activate_process_definition_id(processDefinitionId, includeProcessInstances):
    endpoint = url + "/process-definition/" + processDefinitionId + "/suspended"
    params = {
        "processDefinition": processDefinitionId,
    }
    body = {
        "suspended": "false",
        "includeProcessInstances": includeProcessInstances
        #"date"
    }
    response = requests.request("PUT", endpoint, params=params, json=body)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def suspend_process_definition_key(processDefinitionKey, includeProcessInstances):
    endpoint = url + "/process-definition/suspended"
    body = {
        "processDefinitionKey": processDefinitionKey,
        "suspended": "true",
        "includeProcessInstances": includeProcessInstances
    }
    response = requests.request("PUT", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    elif(response.status_code == 400):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def activate_process_definition_key(processDefinitionKey, includeProcessInstances):
    endpoint = url + "/process-definition/suspended"
    body = {
        "processDefinitionKey": processDefinitionKey,
        "suspended": "false",
        "includeProcessInstances": includeProcessInstances
    }
    response = requests.request("PUT", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    elif(response.status_code == 400):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def update_process_definition_id(id): #used for Za brisanje iz baze
    endpoint = url + "/process-defintion/" + id + "/history-time-to-live"
    response = requests.request("PUT", endpoint)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    elif(response.status_code == 400):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def suspend_process_instance_by_process_definition(id):
    endpoint = url + "/process-instance/" + id + "/suspended"
    body = {
        "suspended": "true"
    }
    response = requests.request("PUT", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def activate_process_instance_by_process_definition(id):
    endpoint = url + "/process-instance/" + id + "/suspended"
    body = {
        "suspended": "false"
    }
    response = requests.request("PUT", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def suspend_process_instance_by_process_definition_key(processDefinitionKey):
    endpoint = url + "/process-instance/suspended"
    body = {
        "processDefinitionKey": processDefinitionKey,
        "suspended": "true"
    }
    response = requests.request("PUT", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def activate_process_instance_by_process_definition_key(processDefinitionKey):
    endpoint = url + "/process-instance/suspended"
    body = {
        "processDefinitionKey": processDefinitionKey,
        "suspended": "false"
    }
    response = requests.request("PUT", endpoint, json=body)
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

def get_process_instance_variables_list(id, deserializeValue):
    endpoint = url + "/process-instance/" + id + "/variables"
    params = {
        "deserializeValue": deserializeValue
    }
    response = requests.request("GET", endpoint, params=params)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_process_instance_variable_binary(id, varName): #not tested, no binary data for testing
    endpoint = url + "/process-instance/" + id + "/variables/" + varName + "/data"
    response = requests.request("GET", endpoint)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def update_process_instance_variable(id, varName, value, varType):
    endpoint = url + "/process-instance/" + id + "/variables/" + varName
    body = {
        "value": value,
        "type": varType,
        #"valueInfo": valueInfo 
    }
    response = requests.request("PUT", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def delete_process_instance_variable(id, varName):
    endpoint = url + "/process-instance/" + id + "/variables/" + varName
    response = requests.request("DELETE", endpoint)
    if(response.status_code == 204):
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

def claim_task(id, userId):
    endpoint = url + "/task/" + id + "/claim"
    body = {
        "userId": userId
    }
    response = requests.request("POST", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def unclaim_task(id):
    endpoint = url + "/task/" + id + "/unclaim"
    response = requests.request("POST", endpoint)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def set_asignee(id, userId):
    endpoint = url + "/task/" + id + "/assignee"
    body = {
        "userId": userId
    }
    response = requests.request("POST", endpoint, json=body)
    if(response.status_code == 204):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_task_formkey(id): # fali path za spajanje forme
    endpoint = url + "/task/" + id + "/form"
    response = requests.request("GET", endpoint)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_deployed_form(id):
    endpoint = url + "/task/" + id + "/deployed-form"
    response = requests.request("GET", endpoint)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
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
        return jsonify(response.text, response.status_code)
    elif(response.status_code == 400):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def get_task_form_variables(id, deserializeValues): 
    endpoint = url + "/task/" + id + "/form-variables"
    params = {
        #"variableNames": variableNames, #moze i bez toga, struktura podataka je lista  variableNames,
        "deserializeValues": deserializeValues
    }
    response = requests.request("GET", endpoint, params=params)
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
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
    if(response.status_code == 200):
        return jsonify(response.text, response.status_code)
    else:
        return jsonify(response.text, response.status_code)

def complete_external_task(id, workerId, kwargs):
    endpoint = url + "/external-task/" + id + "/complete"
    body = {
        "workerId": workerId,
        "variables": {"value": kwargs, "type": kwargs}
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


# def complete_task(id):                                #Mozda rijesiti vanjskom formom, ja se iskreno nadam
#     endpoint = url + "/task/" + id + "/complete"
#     pepe = uzmi_varijable()
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
#         return jsonify(response.text, response.status_code)
#     else:
#         error = jsonify(response.text, response.status_code)
#         return error


#handle external task error
###### TESTIRANJE
@app.route("/api", methods=["GET", "POST", "DELETE", "PUT"])
# def nesto9():
#     calls = get_process_instances_list("mentor_odlucuje:1f5b763f-dc7a-11ea-81b4-60f262e99a90")
#     return calls
def nestoosmo():
    calls = get_activity_tree("c7866b12-dc79-11ea-81b4-60f262e99a90")
    return calls

# def nestosedmo():
#     calls = get_subprocesses("c7866b12-dc79-11ea-81b4-60f262e99a90")
#     return calls   
# def nesto31(): "PrijavaZavrsnogRada", "1f5b763f-dc7a-11ea-81b4-60f262e99a90" "multiInstanceBody"
#     calls = complete_task("f6ea7551-da54-11ea-8fe7-60f262e99a90") "1f5b763f-dc7a-11ea-81b4-60f262e99a90"  ,"nada","true","definitionKey","desc"
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

#post task variable binary
#delete task variable binary
#update task variable

#@app.route('/api/uzmiVarijable', methods=['POST'])
# @cross_origin()
# def uzmi_varijable():
#     varijable = request.get_json()
#     return varijable 

#dummy data
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
# def nesto35():
#     calls = get_task_form_variables("f7b7f6ba-da62-11ea-8fe7-60f262e99a90", True)
#     return calls
# def nesto36():
#     calls = set_asignee("f7b7f6ba-da62-11ea-8fe7-60f262e99a90", "ToniID")
#     return calls
# def nesto37():
#     calls = get_task_variable("7aa6d274-d99c-11ea-b794-60f262e99a90", "Odgovor", True)
#     return calls
# def nesto38():
#     calls = get_task_variables("7aa6d274-d99c-11ea-b794-60f262e99a90", True)
#     return calls
# def nesto39():
#     calls = update_task_variable("8d36fe1f-da58-11ea-8fe7-60f262e99a90", "Naslov", "Peperoncino", "String")
#     return calls
# def nesto40():
#    calls = get_external_tasks("test1")
#    return calls
# def nesto41():
#     calls = fetch_and_lock("default", 1, "test1")
#     return calls
# def nesto42():
#     data = {"value": "Pepe", "type": "String"}
#     calls1 = complete_external_task("38e1716c-db40-11ea-9959-60f262e99a90", "default", data)
#     return calls