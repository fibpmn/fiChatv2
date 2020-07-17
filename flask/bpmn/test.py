import Camunda
import json

worker = Camunda.client("http://localhost:8080/engine-rest", "test")
loop = True

while loop:
    choose = input("Odaberi skriptu: ")
    choose = int(choose)
    if choose == 1:
        print("Startanje procesa...")
        worker.startprocessinstance("ideja2", "default")
    elif choose == 2:
        #worker.correlateamessage("Saljem", "default", "", True, "", True)
        worker.subscribe("Posalji")
        #worker.complete()
        #worker.correlateamessage2("Saljem", True, None )
        #vars = {"assignee": ["MojID"]} "Posalji", , "Default", False
        #worker.complete()
    elif choose == 3:
        worker.subscribe("Napuni")
        vars = {"assigneeList": ["NikolaID", "DarkoID", "TihomirID"]}
        worker.complete(**vars)
    elif choose == 4:
        worker.subscribe("Odluci")
        print("Tema u redu?")
        odluka = input("1/0")
        odluka = int(odluka)
        v = {"odluka": True}
        if odluka == 1:
            worker.complete(**v)
            print("proslo je")
        elif odluka == 0:
            worker.error("Bpmn error")
            print("Tema nije odobrena")
            loop = False
    elif choose == 5:
        #worker.subscribe("pps1")
        worker.correlateamessage("Javise", "t", "", True, "", True)
        #messagename Javise
        #worker.complete()
    elif choose == 6:
        worker.subscribe("ppp1")
        #messagename Javiosamse
        worker.complete()
    elif choose == 7:
        worker.subscribe("pps2")
        #messagename Nijelose
        worker.complete()
    elif choose == 8:
        worker.getprocessvariable("0eece66d-9855-11ea-938b-5a00e348d211", "")
    elif choose == 9:
        worker.subscribe("Zaprimi")
        worker.complete()
    elif choose == 10:
        worker.subscribe("bucibuci")
        #message Prijavljeno
        worker.complete()
    elif choose == 11:
        print("Kraj")
        loop = False
    elif choose == 12:
        worker.getexecution("9b9ce6a4-8f9d-11ea-b31b-5a00e348d211")
    elif choose == 13:
        worker.getactivityinstance("9b9ce6a4-8f9d-11ea-b31b-5a00e348d211")
    elif choose == 14:
        worker.getmessageeventsubscription("Event_1wa7wpe:24054021-8f9e-11ea-b31b-5a00e348d211", "Saljem")
    elif choose == 15:
        #vars = {"assigneeList": ["NikolaID", "DarkoID", "TihomirID"]}
        #worker.complete(**vars)
        varss = {'vars': open('C:/Users/Toni/Desktop/ideja2.bpmn', 'rb')}
        #vars = {"deploymentsource": open("C:/Users/Toni/Desktop/ideja2.bpmn", "rb").read()}
        #vars = {"deploymentsource": v}
        #v = {"deployment-name": "ideja2.bpmn"}
        #worker.processdeployment(**varss)
        worker.processdeployment(**varss)

    elif choose == 16:
        worker.report_get_deployed_form("ispuniprijedlog")
    elif choose == 17:
        worker.report_get_task_form_variables("ispuniprijedlog")
    elif choose == 18:
        worker.report_get_task_form("ispuniprijedlogkey")
    elif choose == 19:
        worker.get_task("posaljiprijedlog")
    else:
        print("Nema odabrane funkcionalnosti")
