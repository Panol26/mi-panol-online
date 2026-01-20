import streamlit as st
from st_supabase_connection import SupabaseConnection
from datetime import datetime

# 1. CONEXIÓN A LA NUBE
st.set_page_config(page_title="Pañol Profesional", layout="wide")

# Reemplaza esto con tus datos de Supabase
URL = "https://ohhjevkgpfigsriadvmj.supabase.co"
KEY = "sb_publishable_N5ziFS4ShJI9GlaRrORfBA_kQWavEVp"

conn = st.connection("supabase", type=SupabaseConnection, url=URL, key=KEY)

# --- ESTILOS ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("🛠️ Menú de Control")
menu = st.sidebar.radio("Ir a:", ["Dashboard", "Inventario", "Préstamos", "Empleados"])

# --- FUNCIONES DE BASE DE DATOS ---
def obtener_datos(tabla):
    return conn.table(tabla).select("*").execute()

def insertar_dato(tabla, dato):
    conn.table(tabla).insert(dato).execute()
    st.rerun()

# --- SECCIONES ---
if menu == "Dashboard":
    st.header("📊 Tablero de Alertas")
    res = obtener_datos("inventario")
    if res.data:
        for item in res.data:
            if item['stock'] <= item['minimo']:
                st.error(f"🚨 REPOSICIÓN: {item['item']} | Stock actual: {item['stock']} (Mínimo: {item['minimo']})")
    else:
        st.info("No hay datos cargados aún.")

elif menu == "Inventario":
    st.header("📦 Gestión de Stock")
    
    # Formulario para agregar
    with st.expander("➕ Cargar Nuevo Artículo"):
        n = st.text_input("Nombre")
        s = st.number_input("Stock Inicial", min_value=0)
        m = st.number_input("Alerta cuando queden:", min_value=1)
        if st.button("Guardar"):
            insertar_dato("inventario", {"item": n, "stock": s, "minimo": m})

    # Mostrar tabla
    res = obtener_datos("inventario")
    if res.data:
        st.table(res.data)

elif menu == "Préstamos":
    st.header("📋 Seguimiento de Préstamos")
    # Aquí puedes hacer la lógica de tiempo
    st.write("Registra aquí quién se lleva las herramientas.")
    # (Similar a la versión anterior pero usando insertar_dato("prestamos", ...))

elif menu == "Empleados":
    st.header("👥 Personal")
    res_e = obtener_datos("empleados")
    # Mostrar y agregar empleados