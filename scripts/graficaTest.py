import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -----------------------------
# 1️⃣ Generar datos de ejemplo
# -----------------------------
np.random.seed(42)
fechas = pd.date_range("2024-01-01", "2024-12-31", freq="D")
regiones = ["Norte", "Sur", "Este", "Oeste", "NE"]
productos = ["Laptop", "Teléfono", "Tablet", "Monitor"]

data = {
    "fecha": np.random.choice(fechas, 1000),
    "region": np.random.choice(regiones, 1000),
    "producto": np.random.choice(productos, 1000),
    "ventas": np.random.randint(100, 5000, 1000)
}
df = pd.DataFrame(data)

# -----------------------------
# 2️⃣ Barra lateral: parámetros
# -----------------------------
st.sidebar.header("📊 Filtros")

region_sel = st.sidebar.multiselect("Selecciona región:", regiones, default=regiones)
producto_sel = st.sidebar.multiselect("Selecciona producto:", productos, default=productos)
rango_fechas = st.sidebar.date_input("Rango de fechas:", [df["fecha"].min(), df["fecha"].max()])

# -----------------------------
# 3️⃣ Filtrar datos 
# -----------------------------
df_filtrado = df[
    (df["region"].isin(region_sel)) &
    (df["producto"].isin(producto_sel)) &
    (df["fecha"].between(pd.to_datetime(rango_fechas[0]), pd.to_datetime(rango_fechas[1])))
]

# -----------------------------
# 4️⃣ Visualizaciones
# -----------------------------
st.title("📈 Dashboard de Ventas Interactivo")

col1, col2 = st.columns(2)
with col1:
    total_ventas = int(df_filtrado["ventas"].sum())
    st.metric("Ventas Totales", f"${total_ventas:,.0f}")
with col2:
    promedio = int(df_filtrado["ventas"].mean())
    st.metric("Promedio de Venta", f"${promedio:,.0f}")

# Gráfico de barras por producto
fig1 = px.bar(
    df_filtrado.groupby("producto", as_index=False)["ventas"].sum(),
    x="producto", y="ventas", color="producto",
    title="Ventas por Producto"
)
st.plotly_chart(fig1, use_container_width=True)

# Gráfico de línea temporal
fig2 = px.line(
    df_filtrado.groupby("fecha", as_index=False)["ventas"].sum(),
    x="fecha", y="ventas",
    title="Evolución de Ventas en el Tiempo"
)
st.plotly_chart(fig2, use_container_width=True)

# Tabla final
st.dataframe(df_filtrado.sort_values("fecha", ascending=False))

st.caption("💡 Puedes ajustar los filtros en el panel lateral para explorar los datos.")
