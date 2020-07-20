import requests
import json
import time


class client:
    def __init__(self, url, workerid="defaultid"):
        self.url = url
        self.workerid = workerid

    def subscribe(self, topic, lockDuration=1000, longPolling=5000):
        endpoint = str(self.url) + '/external-task/fetchAndLock'
        workerid = str(self.workerid)

        task = {"workerId": workerid,
                "maxTasks": 1,
                "usePriority": "true",
                "asyncResponseTimeout": longPolling,
                "topics":
                    [{"topicName": topic,
                      "lockDuration": lockDuration
                      }]
                }

        # Make the request
        global engine
        engine = True
        try:
            fetch_and_lock = requests.post(endpoint, json=task)
            print(fetch_and_lock.status_code)
            global body
            body = fetch_and_lock.text
        except:
            engine = False
            print("Engine is down")
            if (engine == True):
                while body == '[]':
                    print("polling")
                    fetch_and_lock = requests.post(endpoint, json=task)
                    body = fetch_and_lock.text
                    time.sleep(5)
                    if body != '[]':
                        break

    def complete(self, **kwargs):
        response_body = json.loads(body)
        taskid = response_body[0]['id']
        taskid = str(taskid)

        endpoint = str(self.url) + "/external-task/" + taskid + "/complete"

        # get workerid
        workerid = response_body[0]['workerId']
        workerid = str(workerid)

        # puts the variables from the dictonary into the nested format for the json response
        variables_for_response = {}
        for key, val in kwargs.items():
            variable_new = {key: {"value": val}}
            variables_for_response.update(variable_new)

        response = {"workerId": workerid,
                    "variables": variables_for_response
                    }

        try:
            complete = requests.post(endpoint, json=response)
            body_complete = complete.text
            print(body_complete)
            print(complete.status_code)

        except:
            print('fail')

    def error(self, bpmn_error, error_message="not defined", **kwargs):

        response_body = json.loads(body)
        taskid = response_body[0]['id']
        taskid = str(taskid)
        endpoint = str(self.url) + "/external-task/" + taskid + "/bpmnError"
        workerid = response_body[0]['workerId']
        workerid = str(workerid)
        variables_for_response = {}
        for key, val in kwargs.items():
            variable_new = {key: {"value": val}}
            variables_for_response.update(variable_new)
        response = {
            "workerId": workerid,
            "errorCode": bpmn_error,
            "errorMessage": error_message,
            "variables": variables_for_response
        }
        try:
            error = requests.post(endpoint, json=response)
            print(error.status_code)
        except:
            print('fail')

    def fail(self, error_message, retries=0, retry_timeout=0):
        response_body = json.loads(body)
        taskid = response_body[0]['id']
        taskid = str(taskid)
        endpoint = str(self.url) + "/external-task/" + taskid + "/failure"
        workerid = response_body[0]['workerId']
        workerid = str(workerid)
        response = {
            "workerId": workerid,
            "errorMessage": error_message,
            "retries": retries,
            "retryTimeout": retry_timeout}
        try:
            fail = requests.post(endpoint, json=response)
            print(fail.status_code)
        except:
            print('fail')

    def new_lockduration(self, new_duration):
        response_body = json.loads(body)
        taskid = response_body[0]['id']
        taskid = str(taskid)
        endpoint = str(self.url) + "/external-task/" + taskid + "/extendLock"
        workerid = response_body[0]['workerId']
        workerid = str(workerid)
        response = {
            "workerId": workerid,
            "newDuration": new_duration
        }
        try:
            newDuration = requests.post(endpoint, json=response)
            print(newDuration.status_code)
            print(workerid)
        except:
            print('fail')

    def getprocessvariable(self, processid, processvarname):
        task = {
            "id": processid,
            "varName": processvarname
        }
        starturl = str(self.url) + "/process-instance/" + processid + "/variables/" + processvarname
        try:
            start = requests.get(starturl, json=task)
            body_start = start.text
            print(body_start)
            print(start.status_code)
        except:
            print("Failed to Get Process Variable")
            
    def correlateamessage2(self, messageName, resultEnabled, processVariables):
        endpoint = str(self.url) + "/message"
        response = {
            "messageName": messageName,
            "resultEnabled": resultEnabled,
            "processVariables": processVariables
        }
        try:
            start = requests.post(endpoint, json=response)
            body_start = start.text
            print(body_start)
            print(start.status_code)
        except:
            print("Send message failed")

    def correlateamessage(self, messageName, businessKey, CorrelationKeys, withouttenantid, processVariables, resultEnabled):
        endpoint = str(self.url) + "/message"
        response = {
            "messageName": messageName,
            "businessKey": businessKey,
            "CorrelationKeys": {
                CorrelationKeys: {"value": "value", "type": "String"}
            },
            "withoutenantid": withouttenantid,
            "processVariables": {
                processVariables: {"value": "value",
                                   "type": "String",
                                   "valueInfo": {"transient": True},
                                   },
            },
            "resultEnabled": resultEnabled,
            # "processinstanceid": processinstanceid, , processinstanceid
        }
        try:
            start = requests.post(endpoint, json=response)
            body_start = start.text
            print(body_start)
            print(start.status_code)
        except:
            print("Send message failed")

    def getmessageeventsubscription(self, messageid, messageName):
        task = {
            "id": messageid,
            "messageName": messageName
        }
        starturl = str(self.url) + "/execution/" + messageid + "/messageSubscriptions/" + messageName
        try:
            start = requests.get(starturl, json=task)
            body_start = start.text
            print(body_start)
            print(start.status_code)
        except:
            print("Failed to Get Message Subscription")

    def getexecution(self, id):
        task = {
            "id": id,
        }
        starturl = str(self.url) + "/execution/" + id
        try:
            start = requests.get(starturl, json=task)
            body_start = start.text
            print(body_start)
            print(start.status_code)
        except:
            print("Failed to Get Process Variable")

            #GET / process - instance / {id} / activity - instances
    def getactivityinstance(self, id):
        task = {
            "id": id
        }
        starturl = str(self.url) + "/process-instance/" + id + "/activity-instances"
        try:
            start = requests.get(starturl, json=task)
            body_start = start.text
            print(body_start)
            print(start.status_code)
        except:
            print("Failed to Get Process Variable")

    def startprocessinstance(self, processid, businessKey):
        task = {"businessKey": businessKey}
        starturl = str(self.url) + "/process-definition/key/" + processid + "/start"
        try:
            start = requests.post(starturl, json=task)
            body_start = start.text
            print(body_start)
            print(start.status_code)

        except:
            print('failed to start')

    def processdeployment(self, **deploymentsource):
        task = {
            #"deployment-name": deploymentname,
            "deployment-source": deploymentsource
        }
        starturl = str(self.url) + "/deployment/create"
        #try:
        start = requests.post(starturl, json=task)
        body_start = start.text
        print(body_start)
        print(start.status_code)
        #except:
            #print("Failed to deploy")

    def getgroup(self, groupid):
        task = {
            "group-id": groupid
        }
        starturl = str(self.url) + "/group"
        try:
            start = requests.get(starturl, json=task)
            body_start = start.text
            print(body_start)
            print(start.status_code)
        except:
            print("Failed to deploy")

    def identitylink(self, id, groupid, grouptype):
        task = {
            "groupId": groupid,
            "type": grouptype
        }
        starturl = str(self.url) + "/task/" + id + "/identity-links"

    def useridentitylink(self, id, userid, usertype):
        task = {
            "groupId": userid,
            "type": usertype
        }
        starturl = str(self.url) + "/task/" + id + "/identity-links"

    def report_get_deployed_form(self, formid):
        task = {
            "id": formid
        }
        starturl = str(self.url) + "/task/" + formid + "/deployed-form"
        try:
            start = requests.get(starturl, json=task)
            body_start = start.text
            print(body_start)
            print(start.status_code)
        except:
            print("Failed to Get Deployed Form")

    def report_get_task_form_variables(self, id):
        task = {
            "id": id
        }
        starturl = str(self.url) + "/task/" + id + "/form-variables"
        try:
            start = requests.get(starturl, json=task)
            body_start = start.text
            print(body_start)
            print(start.status_code)
        except:
            print("Failed to Get Deployed Form Variables")

    def report_get_task_form(self, id):
        task = {
            "id": id
        }
        starturl = str(self.url) + "/task/" + id + "/form"
        try:
            start = requests.get(starturl, json=task)
            body_start = start.text
            print(body_start)
            print(start.status_code)
        except:
            print("Failed to Get Deployed Form")

    def get_task(self, id):
        task = {
            "id": id
        }
        starturl = str(self.url) + "/task/" + id
        try:
            start = requests.get(starturl, json=task)
            body_start = start.text
            print(body_start)
            print(start.status_code)
        except:
            print("Failed to Get Task")
