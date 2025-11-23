import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import sum, avg,col,first,when,udf,regexp_replace,to_timestamp,trim,split,when,size
from pyspark.sql.types import StringType, DoubleType, ArrayType
import re,sys,json,time

inicio = time.time()
ss = SparkSession.builder.config("spark.jars", "/home/jrodarte/postgresql-42.7.3.jar").getOrCreate()

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
        .option("dbtable", ) \
        .option("user", user) \
        .option("password", password) \
        .option("driver", "org.postgresql.Driver") \
        .load()
    print("Se consultan las fechas que se usarán para los filtros...")
except Exception as inst:
    print(type(inst))    # the exception type
    print(inst.args)     # arguments stored in .args
    print(inst) 


try:
    dfMovimientos = ss.read.format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/postgres") \
        .option("dbtable", ) \
        .option("user", user) \
        .option("password", password) \
        .option("driver", "org.postgresql.Driver") \
        .load()
    
    dfNombreUsuario = dfMovimientos.select('nombre_usuario_solicitante').distinct()
    regTODOS = Row(nombre_usuario_solicitante = "TODOS")
    dfNombreUsuario = dfNombreUsuario.union(ss.createDataFrame([regTODOS]))
    dfMovCount = dfMovimientos.count()
    print(f"Se consultan los movimientos... COUNT {{{dfMovCount}}}")
except Exception as inst:
    print(type(inst))    # the exception type
    print(inst.args)     # arguments stored in .args
    print(inst)   

st.sidebar.header("📊 Filtros")


hoy = pd.to_datetime("today").normalize()
fecha_hace_12_meses = hoy - pd.DateOffset(months=12)

listTipoMovimientos = dfTipoMovimientos.select("tipomovimiento").rdd.flatMap(lambda x: x).collect()
listUsuariosSolicitantes = dfNombreUsuario.select("nombre_usuario_solicitante").rdd.flatMap(lambda x: x).collect()
tipoMov_sel = st.sidebar.multiselect("Selecciona el tipo de movimiento:", listTipoMovimientos, default=["PAGOS"])
rango_fechas = st.sidebar.date_input("Rango de fechas:", [fecha_hace_12_meses,hoy])
add_selectbox = st.sidebar.selectbox("Nombres de usuarios solicitantes:",listUsuariosSolicitantes)

condicion = (
    (dfMovimientos["tipomovimiento"].isin(tipoMov_sel)) &
    (dfMovimientos["feoperacion"].between(pd.to_datetime(rango_fechas[0]), pd.to_datetime(rango_fechas[1])))
)

if add_selectbox != 'TODOS':
    condicion = condicion & (dfMovimientos["nombre_usuario_solicitante"] == add_selectbox)

df_filtrado = dfMovimientos.filter(condicion)

# Gráfico de barras por producto
fig1 = px.bar(
    df_filtrado.groupBy("feoperacion").agg(sum("importe").alias("importe_sum")),
    x="feoperacion", y="importe_sum", color="feoperacion",
    title="Movimientos por mes"
)
st.plotly_chart(fig1, use_container_width=True)

# Tabla final
st.dataframe(df_filtrado.orderBy("feoperacion").limit(2000).toPandas())
