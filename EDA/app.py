import numpy as np
import pandas as pd
from utils import *
import streamlit as st 
import plotly.express as px

# Configuramos el dashboard
st.set_page_config(
    page_icon="../img/logo.png",
    page_title="InmoPipeline",
    layout="wide"
)

def add_icon(tipe:str) -> str:
    """ Funcion para agregar iconos """
    icon = f":material/{tipe}:"
    return  icon

# Definimos la url donde esta nuestro modelo
URL_MODEL = "http://127.0.0.1:8000/model"

# Definimos el titulo del dashboard
st.header("🏡 FincaRaiz - Exploración del Mercado de Bienes Raíces en Colombia",width="content")
st.caption("Análisis exploratorio de precios y ubicación de propiedades en Colombia")

# Cargamos el dataframe
@st.cache_data() # Guardamos en cache los datos
def get_data():
    df = pd.read_csv("../Data/propiedades.csv")
    return df

df = get_data()
df_ordenado = ["ciudades","region","precios","habitaciones","baños","metros_cuadrados","enlaces"]

# Personalizamos el estilo de los datos que se mostraran
df_column_style = {
            "enlaces":st.column_config.LinkColumn("Enlaces",help="Enlaces de cada inmueble"),
            
            "ciudades":st.column_config.TextColumn("Ciudades",help="Ciudad donde esta el inmueble"),
            
            "region":st.column_config.ListColumn("Regiones",help="Region de cada ciudad"),
            
            "precios":st.column_config.NumberColumn("Precios",format="compact",width="small",help="Valor del inmueble"),
            
            "habitaciones":st.column_config.NumberColumn("Habitaciones",format=f"%d 🏠",width="small",help="Numero de habitaciones en el inmueble"),
            
            "baños":st.column_config.NumberColumn("Baños",format="%d 🚽",width="small",help="Numero de baños en el inmueble"),
            
            "metros_cuadrados":st.column_config.NumberColumn("M²",width="small",format="%d M²",help="Metros cuadrados del inmueble")
            }

# _________________ Primera configuracion del sidebar __________________________
# Definimos el primer sidebar para filtrar
with st.sidebar:
    st.logo("https://cdn-icons-png.flaticon.com/128/14648/14648421.png",size="large")
    st.image("../img/logo.png")
    st.subheader("Configuraciones",divider="orange")
    
    # Filtramos por top interactivo
    top = int(st.number_input(label="Digite el numero de top a mostrar",
                        value=5, min_value=3, max_value=10, step=1, format="%d", icon=add_icon("swap_vert"),help="Limita el numero de resultados mayores"))
    
    # Filtrar por regiones
    lista_regiones = df["region"].sort_values().unique()
    regiones = st.multiselect("Selecione regiones",lista_regiones,placeholder="Seleccione una mas regiones")
        
    # Filtramos el dataframe solo para definir las ciudades disponibles
    if regiones:
        df_ciudades_disponibles = df[df["region"].isin(regiones)]
    else:
        df_ciudades_disponibles = df
        
    # Filtrar por ciudades
    lista_ciudades = df_ciudades_disponibles["ciudades"].sort_values().unique()
    ciudades: list = st.multiselect("Selecionar ciudades",lista_ciudades,placeholder="Seleccione una o mas ciudades")
        
    # Definimos el tipo de correlacion para el mapa de calor
    correlaciones = ['spearman','pearson', 'kendall']
    metodo_corr = st.selectbox("Metoodo de correlacion",correlaciones,help="Seleccione el metodo de correlacion que se aplicara el mapa de calor")
    
    # Check para filtrar terrenos sin habitaciones ni baños
    filtro_terrenos = st.toggle("Excluir valores desconocidos",help="Elimina los valores desconocidos de cada columna")
    

# ______________________ Filtros __________________________________________
if filtro_terrenos:
    # Limpiamos los valores nulos
    df = df[
        (df["habitaciones"]>0) & 
        (df["baños"]>0) & 
        (df["ciudades"] != "no especifica") &
        (df["region"] != "desconocido")
        ]
    
    st.toast("Se eliminaron los datos con valores incompletos",icon=add_icon("delete"))
    
if regiones:
    df = df[df["region"].isin(regiones)]
    regiones_texto = ", ".join(regiones)
    st.toast(f"Regiones :green[{str(regiones_texto)}] selecionadas de manera correcta",icon=add_icon("map"))

if ciudades:
    df = df[df["ciudades"].isin(ciudades)]
    st.toast(f":green[{len(ciudades)}] Ciudades selecionadas con exito",icon=add_icon("location_city"))

# Reset index después de todos los filtros
df = df.reset_index(drop=True)
if df.empty:
    st.badge("Sin resultados para los filtros seleccionados", icon=add_icon("warning"),color="red")
    st.error("⚠️ No hay datos disponibles con los filtros seleccionados. Por favor, ajuste los filtros.")
    st.stop()  # Detiene la ejecución del resto del código
    
    
# ___________________________ Continuacion de sidebar ___________________________-
# Volvemos a llamar al sidebar post modificaciones
with st.sidebar:
    st.subheader("Funciones extra",divider="orange")
    
    if st.button("Predecir",icon=add_icon("model_training"),use_container_width=True,help="Realiza predicciones del precio del inmueble en base a sus parametros"):
        predict_price(df)
        st.toast(":green[Entro en modo de prediccion]",icon=add_icon("check"))
        
    if st.button("Resumen",icon=add_icon("description"),use_container_width=True,help="Obtenga un resumen estadictico general de los datos"):
        describe_data(df)
        st.toast(":green[Resumen generado]",icon=add_icon("description"))
        
    st.subheader("Fuentes de datos",divider="orange")
    
    # Fuente de los datos con enlace real
    st.link_button("Datos - FincaRaiz","https://www.fincaraiz.com.co",icon=add_icon("dataset_linked"),use_container_width=True,type="primary")
    
    st.link_button("API Colombia - Regiones","https://api-colombia.com",use_container_width=True,icon=add_icon("api"),type="primary")
    
    
# ___________________________ badge de estado de filtros ________________________
# Mostramos datos de filtro
c1,c2,c3,c4 = st.columns(4)
with c1: 
    if regiones:
        st.badge(f"Regiones filtradas: {len(regiones)}", icon=add_icon("map"), color="orange")
    else:
        st.badge(f"Regiones totales: {len(df['region'].unique())}", icon=add_icon("map"), color="green")
        
with c2:
    if ciudades:
        st.badge(f"Ciudades filtradas: {len(ciudades)}", icon=add_icon("location_city"), color="orange") 
    else:
        st.badge(f"Ciudades: {len(df['ciudades'].unique())}", icon=add_icon("location_city"), color="green") 
with c3:
    if filtro_terrenos:
        st.badge(f"Se excluyeron valores", icon=add_icon("disabled_visible"), color="orange") 
    else:
        st.badge(f"Todos los valores disponibles", icon=add_icon("in_home_mode"), color="green") 
with c4:
    if regiones and ciudades:
        st.badge("Análisis enfocado por región y ciudad", icon=add_icon("search_insights"), color="orange")
    elif regiones:
        st.badge(f"Análisis enfocado por región: {len(regiones)}", icon=add_icon("search_insights"), color="orange")
    elif ciudades:
        st.badge(f"Análisis enfocado por ciudad: {len(ciudades)}", icon=add_icon("search_insights"), color="orange")
    else:
        st.badge("Análisis general - Todo el país", icon=add_icon("search_insights"), color="green")

# _____________________ Manejo de datos __________________________
# Fila de la propiedad más cara y mas barata
prop_mas_cara = df.loc[df["precios"].idxmax()]
prop_men_cara = df.loc[df["precios"].idxmin()]

# Definimos las agrupaciones

# Agrupacion por habitaciones
agrupacion_hab = df.groupby("habitaciones")["precios"].mean().reset_index()
top_hab = agrupacion_hab.nlargest(top,"precios")

# Agrupacion por ciudad
agrupacion_ciudad = df.groupby("ciudades")["precios"].mean().reset_index()
top_ciudades_caras = agrupacion_ciudad.nlargest(top,"precios")
top_ciudades_baratas = agrupacion_ciudad.nsmallest(top,"precios")

# Agrupacion por metros cuadrados
agrupacion_metro = df.groupby("metros_cuadrados")["precios"].mean().reset_index()
top_metros = agrupacion_metro.nlargest(top,"precios")

# Resumen de ciudades
resumen_ciudades = df.groupby("ciudades").agg({
    "precios":"mean",
    "habitaciones":"mean",
    "baños":"mean"
}).reset_index()
top_resumen_ciudades = resumen_ciudades.nlargest(10,"precios")

# Agrupacion por regiones
agrupacion_regiones = df.groupby("region")["precios"].mean().reset_index()
num_propiedades_region = df.groupby("region").size().reset_index(name="propiedades")
top_regiones_caras = agrupacion_regiones.nlargest(top,"precios")

# _______________________ Metricas ___________________________________
# Definimos las metricas importantes
c1,c2,c3,c4 = st.columns(4)
c1.metric(label=f"Mayor precio - {prop_mas_cara['ciudades']}", 
            value=f"${prop_mas_cara['precios']:,.0f}",border=True)

c2.metric(label=f"Menor precio - {prop_men_cara['ciudades']}", 
            value=f"${prop_men_cara['precios']:,.0f}",border=True)

c3.metric("Precio promedio", f"${df['precios'].mean():,.0f}",border=True)

c4.metric("Total de propiedades", df.shape[0],border=True)

# _____________________ Visualizaciones __________________________________
st.subheader("Tabla de datos",divider="orange")

# Mostramos el dataframe
st.dataframe(df,use_container_width=True,
            column_order=df_ordenado,hide_index=True,
            column_config=df_column_style)

# Mostramos las graficas
st.subheader("Graficas",divider="orange")

# Top ciudades caras/baratas
c1,c2 = st.columns(2)
with c1: 
    bar_fig_horizon = px.bar(top_ciudades_caras, x="precios", y="ciudades", 
                            orientation="h",text="precios",color="ciudades",
                            title=f"Top {top} ciudades con mayor precio promedio")
    
    st.plotly_chart(bar_fig_horizon)
with c2:
    bar_fig_horizon = px.bar(top_ciudades_baratas, x="precios", y="ciudades", 
                            orientation="h",text="precios",color="ciudades",
                            title=f"Top {top} ciudades con menor precio promedio")
    
    st.plotly_chart(bar_fig_horizon)

# Habitaciones y correlacion2
c1,c2 = st.columns(2)
with c1:
    bar_fig = px.bar(top_hab,x="habitaciones",y="precios",text="precios",
                    title="Precio promedio segun habitaciones",color="habitaciones",)
    bar_fig.update_yaxes(type="log")
    
    st.plotly_chart(bar_fig)
    
with c2:
    variables = ["precios","metros_cuadrados","habitaciones","baños"]
    df_corr = df[variables].corr(method=metodo_corr)
    # Heatmap con Plotly
    fig = px.imshow(df_corr,
                    text_auto=True,
                    color_continuous_scale='Ice',
                    title=f"Matriz de Correlación - {metodo_corr.title()}")
    st.plotly_chart(fig)

# Regiones 
c1,c2 = st.columns(2)
with c1: 
    top_r = top
    # Limitamos top a > 6
    if top > 5 and filtro_terrenos:
        top_r = 5
    elif top > 6:
        top_r = 6
    bar_fig_horizon = px.bar(top_regiones_caras, x="precios", y="region", 
                            orientation="h",text="precios",color="region",
                            title=f"Top {top_r} regiones con mayor precio promedio")
    
    st.plotly_chart(bar_fig_horizon)
    
with c2:
    fig = px.pie(
    num_propiedades_region,
    values="propiedades",
    names="region",
    title="Distribución de propiedades por región",
    hole=0.3 
    )

    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig)

# Distribucion 
c1,c2 = st.columns(2)
with c1:
    fig = px.area(top_metros.sort_values("metros_cuadrados"), x="metros_cuadrados", y="precios",
                title=f"Top {top} Metros Cuadrados con Mayor Precio Promedio (Área)")
    st.plotly_chart(fig)
with c2:
    df["log_precios"] = np.log(df["precios"])
    hist_fig = px.histogram(df,x="log_precios",nbins=30,
                title="Distribucion de precios de las propiedades",color_discrete_sequence=["#F54B1C"])
    st.plotly_chart(hist_fig)
    

