#!/usr/bin/env python
# coding: utf-8

# In[28]:


from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg,col,first,when,udf,regexp_replace,to_timestamp
from pyspark.sql.types import StringType, DoubleType, ArrayType
import re
ss = SparkSession.builder.config("spark.jars", "/home/jrodarte/postgresql-42.7.3.jar").getOrCreate()


# In[29]:


dfPrestamos = ss.read.format("csv").options(header='true', inferSchema='true', delimiter=',').load("documentos/mis_prestamos020925.csv")
#dfPrestamos.schema


# In[30]:


def parceFecha(fecha):
    if fecha == '0000-00-00':
        return '1900-01-01'
    else:
        return fecha

parceFecha_udf = udf(parceFecha, StringType())


# In[31]:


dfPrestamos = dfPrestamos.withColumn('fecha_liberado', parceFecha_udf(col("fecha_liberado")))
#dfPrestamos.filter(col("fecha_liberado") == '1900-01-01').show()
dfPrestamos = dfPrestamos.withColumn('fecha_liberado', to_timestamp(col("fecha_liberado"), "yyyy-MM-dd"))
#dfPrestamos.show()


# In[27]:


dfPrestamos.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/postgres") \
    .option("dbtable", "prestadero.prestamos") \
    .option("user", "jrodarte") \
    .option("password", "roma1993_") \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()

