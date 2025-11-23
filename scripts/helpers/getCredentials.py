import json

def getCredentialsUser(userName):
    arrUser = []
    # Datos de conexión
    try:
        with open("/home/jrodarte/Proyectos/prestadero/config/credenciales.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        if userName == 'jrodarte':
            user = data["usuario"]
            password = data["pass"]
            estatus = data["activo"]
        else: 
            user = "-"
            password = "-"
            estatus = False
    except Exception as inst:
        print(type(inst))    # the exception type
        print(inst.args)     # arguments stored in .args
        print(inst) 

    arrUser.append(user)
    arrUser.append(password)
    arrUser.append(estatus)

    return arrUser