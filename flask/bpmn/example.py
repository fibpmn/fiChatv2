import Camunda

worker = Camunda.client("http://localhost:8080/engine-rest", "test")
loop = True

while loop:
    choose = input("Odaberi skriptu: ")
    choose = int(choose)
    if choose == 0:
        print("Kraj rada")
        loop = False
    elif choose == 1:
        worker.startprocessinstance("ideja2","default")
    elif choose == 2:
        worker.subscribe("Posalji")
        vars = {"assigneeList": ["NikolaID", "DarkoID", "TihomirID"]}
        worker.complete(**vars)
    elif choose == 3:
        worker.getprocessvariable("0e4dc1b7-907d-11ea-8428-c85b76ae5348", "")
    elif choose == 4:
        #worker.getgroup("Mentori")
        worker.identitylink("Activity_1h1p2x0", "assigneeList", "candidate")
    elif choose == 5:
        worker.subscribe("pepe")
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
    elif choose == 6:
        worker.useridentitylink("5d8c4f8d-9093-11ea-8428-c85b76ae5348", "Tihomir", "candidate")
    else:
        print("Nema odabrane funkcionalnosti")