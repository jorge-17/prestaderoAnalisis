#!/usr/bin/env python
# coding: utf-8


from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg,col,first,when,udf,regexp_replace,to_timestamp
from pyspark.sql.types import StringType, DoubleType, ArrayType
import re
import sys
ss = SparkSession.builder.config("spark.jars", "/home/jrodarte/postgresql-42.7.3.jar").getOrCreate()

if len(sys.argv) > 1:
    nombre = sys.argv[1]
else:
    print("No me diste ningún nombre")

print(f"Se van a procesar los movimientos de la siguiente fecha: {nombre}")
dfMovimientos = ss.read.format("csv").options(header='true', inferSchema='true', delimiter=',').load(f"documentos/movimientos{nombre}.csv")


# Datos de conexión
user = "jrodarte"
password = "roma1993_"

try:
    dfTipoMovimientos = ss.read.format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/postgres") \
        .option("dbtable", "(select * from prestadero.tipomovimientos)") \
        .option("user", user) \
        .option("password", password) \
        .option("driver", "org.postgresql.Driver") \
        .load()
    print("Se consultan los tipos de movimientos...")
except Exception as inst:
    print(type(inst))    # the exception type
    print(inst.args)     # arguments stored in .args
    print(inst)   

def limpiarImporte(importe):
    return importe.replace("$", "").replace(",", "")

limpiarImpoUDF = udf(limpiarImporte, StringType())

nuevosNombresMov = ['autorizacion', 'feoperacion', 'tipo', 'movimiento', 'importe', 'estatus', 'referencia']
nuevosNombresDetMov = ['autorizacion', 'detalle']
dfDetalleMovimiento = dfMovimientos.select('Autorización', 'Detalle')
dfMovimientos = dfMovimientos.selectExpr(
    "`Autorización`",
    "`Fecha operación`",
    "`Tipo`",
    "`Movimiento`",
    "`Importe`",
    "`Estatus`",
    "`Ref. 1`"
)

dfMovimientos = dfMovimientos.toDF(*nuevosNombresMov)
dfMovimientos = dfMovimientos.withColumn('feoperacion', to_timestamp(col("feoperacion"), "dd/MM/yyyy HH:mm:ss"))
dfMovimientos = dfMovimientos.withColumn('importeS', limpiarImpoUDF(col("importe")))
dfMovimientos = dfMovimientos.withColumn('importe', col("importeS").cast(DoubleType())).drop("importeS")
dfDetalleMovimiento = dfDetalleMovimiento.toDF(*nuevosNombresDetMov)

dfMovimientos = dfMovimientos.join(dfTipoMovimientos, dfMovimientos.movimiento == dfTipoMovimientos.tipomovimiento, "inner")
dfMovimientos = dfMovimientos.drop('tipomovimiento').drop('movimiento')
conteoMovimientos = dfMovimientos.count()
print(f"Se finaliza el procesamiento de {conteoMovimientos} movimientos...")

try:
    dfMovimientos.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/postgres") \
        .option("dbtable", "prestadero.movimientos") \
        .option("user", user) \
        .option("password", password) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
    print("Se almaceno exitosamente en base de datos")
except Exception as inst:
    print(type(inst))    # the exception type
    print(inst.args)     # arguments stored in .args
    print(inst)   

