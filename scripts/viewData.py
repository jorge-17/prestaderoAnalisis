import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pyspark.sql import SparkSession
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
        .option("dbtable", "(select tm.tipomovimiento from prestadero.tipomovimientos tm)") \
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
        .option("dbtable", "(select mov.autorizacion, date_trunc('month', mov.feoperacion) as feoperacion, mov.tipo, mov.importe, mov.nombre_usuario_solicitante, t.tipomovimiento from postgres.prestadero.movimientos mov left join prestadero.tipomovimientos t on mov.idtipomovimiento = t.idtipomovimiento)") \
        .option("user", user) \
        .option("password", password) \
        .option("driver", "org.postgresql.Driver") \
        .load()
    
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
tipoMov_sel = st.sidebar.multiselect("Selecciona región:", listTipoMovimientos, default=["PAGOS"])
rango_fechas = st.sidebar.date_input("Rango de fechas:", [fecha_hace_12_meses,hoy])

df_filtrado = dfMovimientos[
    (dfMovimientos["tipomovimiento"].isin(tipoMov_sel)) &
    (dfMovimientos["feoperacion"].between(pd.to_datetime(rango_fechas[0]), pd.to_datetime(rango_fechas[1])))
]

# Gráfico de barras por producto
fig1 = px.bar(
    df_filtrado.groupBy("feoperacion").agg({"importe": "sum"}),
    x="feoperacion", y="sum(importe)", color="feoperacion",
    title="Movimientos por mes"
)
st.plotly_chart(fig1, use_container_width=True)

# Tabla final
st.dataframe(df_filtrado.orderBy("feoperacion").limit(2000).toPandas())
