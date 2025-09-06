#!/usr/bin/env python
# coding: utf-8


from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg,col,first,when,udf,regexp_replace,to_timestamp,trim,split,when,size
from pyspark.sql.types import StringType, DoubleType, ArrayType
import re,sys,json,time

inicio = time.time()
ss = SparkSession.builder.config("spark.jars", "/home/jrodarte/postgresql-42.7.3.jar").getOrCreate()

if len(sys.argv) > 1:
    nombre = sys.argv[1]
else:
    print("No me diste ningún nombre")

print(f"Se van a procesar los movimientos de la siguiente fecha: {nombre}")
dfMovimientos = ss.read.format("csv").options(header='true', inferSchema='true', delimiter=',').load(f"/home/jrodarte/Proyectos/prestadero/documentos/movimientos{nombre}.csv")


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
    return re.sub(r"[^0-9.]", "", importe)

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
dfMovimientos = dfMovimientos.withColumn("nombre_usuario_solicitante",
    when(size(split(col("referencia"), ":")) > 1, trim(split(col("referencia"), ":").getItem(1)))
    .otherwise(None)
)
dfDetalleMovimiento = dfDetalleMovimiento.toDF(*nuevosNombresDetMov)

dfMovimientos = dfMovimientos.join(dfTipoMovimientos, dfMovimientos.movimiento == dfTipoMovimientos.tipomovimiento, "inner")
dfMovimientos = dfMovimientos.drop('tipomovimiento','movimiento')
print(f"Se finaliza el procesamiento de {dfMovimientos.count()} movimientos...")

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

ss.stop()
fin = time.time()
print(f"Tiempo de ejecución: {fin - inicio:.2f} segundos")