#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
import re
import sys
import time
from helpers.getCredentials import getCredentialsUser
from helpers.getDataframeP import getDataframeBD, putDataframeDB

# -------------------------
# INICIO
# -------------------------
inicio = time.time()

# Uso:
# python3 movimientosP.py {{{NombreArchivo}}} jrodarte
if len(sys.argv) > 2:
    nombre = sys.argv[1]
    userNameInput = sys.argv[2]
else:
    print("Uso incorrecto: python3 movimientosP.py <NombreArchivo> <Usuario>")
    sys.exit(1)

# -------------------------
# CREDENCIALES
# -------------------------
arrCredential = getCredentialsUser(userNameInput)

if not arrCredential[2]:
    print("El usuario que ingresaste no tiene permiso o no existe...")
    sys.exit(1)

user = arrCredential[0]
password = arrCredential[1]

print(f"Se van a procesar los movimientos de la siguiente fecha: {nombre}")

# -------------------------
# LIMPIEZA CSV
# -------------------------
ruta_base = "/home/jrodarte/Proyectos/prestadero/documentos"

ruta_original = f"{ruta_base}/movimientos{nombre}.csv"
ruta_limpia = f"{ruta_base}/movimientos{nombre}Cln.csv"

df = pd.read_csv(ruta_original)

df = df.replace(r'\n\s+', '', regex=True)
df = df.replace(r'\n\s+0', ' 0', regex=True)

df.to_csv(ruta_limpia, index=False)

dfMovimientos = df

# -------------------------
# RENOMBRAR Y SELECCIONAR COLUMNAS
# -------------------------
dfDetalleMovimiento = dfMovimientos[['Autorización', 'Detalle']].copy()
dfDetalleMovimiento.columns = ['autorizacion', 'detalle']

dfMovimientos = dfMovimientos[
    [
        'Autorización',
        'Fecha operación',
        'Tipo',
        'Movimiento',
        'Importe',
        'Estatus',
        'Ref. 1'
    ]
]

dfMovimientos.columns = [
    'autorizacion',
    'feoperacion',
    'tipo',
    'movimiento',
    'importe',
    'estatus',
    'referencia'
]

# -------------------------
# FECHAS
# -------------------------
dfMovimientos['feoperacion'] = pd.to_datetime(
    dfMovimientos['feoperacion'],
    format='%d/%m/%Y %H:%M:%S',
    errors='coerce'
)

dfMovimientos['femovimiento'] = dfMovimientos['feoperacion'].dt.date

dfMovimientos['feoperacion_mes'] = (
    dfMovimientos['feoperacion']
    .dt.to_period('M')
    .dt.to_timestamp()
    .dt.date
)

dfMovimientos['feoperacion'] = dfMovimientos['feoperacion_mes']

dfMovimientos.drop(columns=["feoperacion_mes"], inplace=True)

# -------------------------
# LIMPIAR IMPORTE
# -------------------------
dfMovimientos['importe'] = (
    dfMovimientos['importe']
    .astype(str)
    .str.replace(r'[^0-9.]', '', regex=True)
    .replace('', '0')
    .astype(float)
)

# -------------------------
# USUARIO SOLICITANTE
# -------------------------
dfMovimientos['nombre_usuario_solicitante'] = (
    dfMovimientos['referencia']
    .where(dfMovimientos['referencia'].notna())
    .str.split(':')
    .str[1]
    .str.strip()
)

# -------------------------
# TIPO MOVIMIENTOS (BD)
# -------------------------
dfTipoMovimientos = getDataframeBD(
    user,
    password,
    'get.TipoMovimientos'
)

# -------------------------
# JOIN
# -------------------------
dfMovimientos = dfMovimientos.merge(
    dfTipoMovimientos,
    left_on='movimiento',
    right_on='tipomovimiento',
    how='inner'
)

dfMovimientos.drop(
    columns=['tipomovimiento', 'movimiento'],
    inplace=True
)

# -------------------------
# VALIDACIONES
# -------------------------
if dfMovimientos.empty:
    print("⚠️ El DataFrame quedó vacío después del join.")
    sys.exit(1)

print(f"Se finaliza el procesamiento de {len(dfMovimientos)} movimientos...")

# -------------------------
# INSERTAR A BD
# -------------------------
putDataframeDB(
    user,
    password,
    "put.Movimientos",
    dfMovimientos
)

# -------------------------
# FIN
# -------------------------
fin = time.time()
print(f"Tiempo de ejecución: {fin - inicio:.2f} segundos")