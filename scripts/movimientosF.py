#!/usr/bin/env python
# coding: utf-8


from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg,col,first,when,udf,regexp_replace,to_timestamp,trim,split,when,size
from pyspark.sql.types import StringType, DoubleType, ArrayType
import re,sys,json,time
from helpers.getCredentials import getCredentialsUser
from helpers.getDataframe import getDataframeBD, putDataframeDB

inicio = time.time()
if len(sys.argv) > 1:
    nombre = sys.argv[1]
    userNameInput = sys.argv[2]
else:
    print("No me diste ningún nombre")

arrCredential = getCredentialsUser(userNameInput)

if arrCredential[2]:
    ss = SparkSession.builder.config("spark.jars", "/home/jrodarte/postgresql-42.7.3.jar").getOrCreate()
    print(f"Se van a procesar los movimientos de la siguiente fecha: {nombre}")
    dfMovimientos = ss.read.format("csv").options(header='true', inferSchema='true', delimiter=',').load(f"/home/jrodarte/Proyectos/prestadero/documentos/movimientos{nombre}.csv")

    user = arrCredential[0]
    password = arrCredential[1]

    dfTipoMovimientos = getDataframeBD(user, password, 'get.TipoMovimientos', ss)

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

    putDataframeDB(user, password, "put.Movimientos", dfMovimientos)

    ss.stop()
else:
    print("El usuario que ingresaste no tiene permiso o no existe...")
fin = time.time()
print(f"Tiempo de ejecución: {fin - inicio:.2f} segundos")