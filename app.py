import streamlit as st
from st_supabase_connection import SupabaseConnection

st.set_page_config(page_title="Pañol Online", layout="wide")

# Conexión automática usando los Secrets que pusiste
conn = st.connection("supabase", type=SupabaseConnection)

st.title("🛠️ Sistema de Pañol Profesional")

# --- NAVEGACIÓN ---
menu = st.sidebar.selectbox("Seleccionar Sección:", ["📦 Inventario", "👥 Empleados", "📋 Préstamos"])

# --- SECCIÓN INVENTARIO ---
if menu == "📦 Inventario":
    st.header("Control de Stock")
    
    # Formulario para agregar items
    with st.expander("➕ Agregar Nuevo Item al Stock"):
        with st.form("nuevo_item"):
            nombre = st.text_input("Nombre de la herramienta")
            cantidad = st.number_input("Stock inicial", min_value=0)
            alerta = st.number_input("Mínimo para alerta roja", min_value=1)
            botón = st.form_submit_button("Registrar en Base de Datos")
            
            if botón:
                conn.table("inventario").insert({"item": nombre, "stock": cantidad, "minimo": alerta}).execute()
                st.success("¡Guardado correctamente!")
                st.rerun()

    # Mostrar Tabla y Alertas Rojas
    res = conn.table("inventario").select("*").execute()
    if res.data:
        df = pd.DataFrame(res.data)
        
        # Alertas visuales
        for index, row in df.iterrows():
            if row['stock'] <= row['minimo']:
                st.error(f"⚠️ REPOSICIÓN URGENTE: {row['item']} (Quedan {row['stock']})")
        
        st.dataframe(df, use_container_width=True)

# --- SECCIÓN EMPLEADOS ---
elif menu == "👥 Empleados":
    st.header("Registro de Personal")
    with st.form("nuevo_emp"):
        nombre_emp = st.text_input("Nombre Completo")
        if st.form_submit_button("Agregar Empleado"):
            conn.table("empleados").insert({"nombre": nombre_emp}).execute()
            st.success("Empleado registrado")

