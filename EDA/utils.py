import httpx
import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data()
def get_data():
    current_dir = Path(__file__).resolve().parent  # EDA/
    data_path = current_dir.parent / 'Data' / 'propiedades.csv'
    if not data_path.exists():
        st.error("❌ Archivo no encontrado en: " + str(data_path))
        st.stop()

    df = pd.read_csv(data_path)
    return df
    return df

# Definimos la url donde esta nuestro modelo
URL_MODEL = "http://127.0.0.1:8000/model"

@st.dialog("Resumen estadistico",width="large")
def describe_data(df):
    st.subheader("Descripcion estadistica de los datos",divider="orange")
    st.dataframe(df.describe())
    st.caption(":blue[Resumen estaditicos de los datos]")
    
    
def add_icon(tipe:str) -> str:
    """ Funcion para agregar iconos """
    icon = f":material/{tipe}:"
    return  icon

@st.dialog("Predecir precio",width="large")
def predict_price(df):
    """ Realiza una solcitud post a la API que tiene el modelo y devuelve la respuesta"""
    # Definimos la lista de regiones que espera la API
    list_regiones = ["Caribe","Amazonia","Pacífico","Orinoquía","Andina","Insular"]
    
    # Creamos el formulario
    with st.form("Formulario para predecir precio"):
        
        metros_2 = st.number_input("Metros cuadrados",min_value=10.0,icon=add_icon("metro"),help="Indique el numero de metros cuadros que desea analizar",value=100.0,step=0.1)
        
        habs = st.number_input("Numero de habitaciones",min_value=0,icon=add_icon("sensor_door"),help="Indica el numero de habitaciones que quiere")
        
        baños = st.number_input("Numero de baños",min_value=0,icon=add_icon("bathroom"),help="Indica el numero de baños que quiere")
        
        region = st.selectbox("Region",options=list_regiones,help="Indique en que region quiere analizar el inmueble")
        
        # Definimos el boton de enviar
        enviar = st.form_submit_button("Enviar",icon=add_icon("send"),type="primary")
        
        if enviar:
            # Recopilamos los datos
            data = {
                "habs":int(habs),
                "baños": int(baños),
                "m2": float(metros_2),
                "region": str(region)
            }
            
            # Creamos un spinner para esperar a que la API responda
            with st.spinner("Enviando datos y esperando respuesta de la API...",show_time=True):
                # Enviamos los datos y obtenemos la respuesta
                try:
                    # Enviamos los datos
                    response = httpx.post(URL_MODEL,json=data)
                    
                    # Validamos la respuesta del servidor
                    if response.status_code == 200:
                        json_response = response.json() # Obtenemos el body
                        
                        # Seperamos la respuesta
                        prediccion = json_response.get("Prediccion")
                        detalles = json_response.get("Details")
                        
                        # Mostramos la respuesta
                        st.success(f"Prediccion: {prediccion}",icon=add_icon("check_circle"))
                        
                        # Mostramos los detalles
                        with st.expander("Ver detalles",icon=add_icon("content_paste_search")):
                            st.json(detalles,expanded=True)
                        
                except Exception as e:
                    st.error(f"Error al enviar datos: {e}")
    