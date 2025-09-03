#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2


# In[2]:


# Datos de conexión
host = "localhost"
dbname = "postgres"
user = "jrodarte"
password = "roma1993_"
port = 5432  # Puerto por defecto


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




