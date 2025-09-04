#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2,json


# In[2]:


# Datos de conexión
host = "localhost"
dbname = "postgres"
port = 5432  # Puerto por defecto
# Datos de conexión
try:
    with open("/home/jrodarte/Proyectos/prestadero/config/credenciales.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if data["activo"] == True:
        user = data["usuario"]
        password = data["pass"]
except Exception as inst:
    print(type(inst))    # the exception type
    print(inst.args)     # arguments stored in .args
    print(inst) 



# In[8]:


try:
    # Establecer conexión
    conn = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password,
        port=port
    )
    print("✅ Conexión exitosa")

    # Crear un cursor para ejecutar consultas
    cur = conn.cursor()

    # Ejecutar una consulta
    cur.execute("select * from prestadero.usuario;")
    version = cur.fetchone()
    print("Versión de PostgreSQL:", version)

    # Cerrar cursor y conexión
    cur.close()
    conn.close()

except Exception as e:
    print("❌ Error al conectar a PostgreSQL:", e)


# In[ ]:




