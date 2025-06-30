import numpy as np
import pandas as pd
import streamlit as st 
import plotly.express as px


# Configuramos el dashboard
st.set_page_config(
    page_icon="https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-6F0Oea8suMLdEi6BoluXYbqXxnWEdt.png&w=1920&q=75",
    page_title="InmoPipeline",
    layout="wide"
)

# Definimos el titulo del dashboard
st.title("🏡 FincaRaiz - Exploración del Mercado de Bienes Raíces en Colombia")
st.caption("Análisis exploratorio de precios y ubicación de propiedades en Colombia")

# Cargamos el dataframe
df = pd.read_csv("../Data/propiedades.csv")
df_ordenado = ["ciudades","region","precios","habitaciones","baños","metros_cuadrados","enlaces"]


# Definimos el sidebar
with st.sidebar:
    st.image("https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-YxKlwIcjJqTAeRHzfEN0Qra6tvwzNQ.png&w=1920&q=75")
    st.subheader("Configuraciones",divider="red")
    
    # Filtramos por top interactivo
    top = int(st.number_input(label="Digite el numero de top a mostrar",
                        value=5, min_value=3, max_value=10, step=1, format="%d", icon="🏆",help="Limita el numero de resultados mayores"))
    

    # Filtrar por ciudades
    lista_ciudades = df["ciudades"].sort_values().unique()
    ciudades: list = st.multiselect("Selecionar ciudades",lista_ciudades)
    
    # Filtrar por regiones
    lista_regiones = df["region"].sort_values().unique()
    regiones = st.multiselect("Selecione regiones",lista_regiones)
    
    # Check para filtrar terrenos sin habitaciones ni baños
    filtro_terrenos = st.checkbox("Excluir valores desconocidos",help="Elimina los valores desconocidos de cada columna")
    
    st.subheader("Fuentes de datos",divider="red")
    # Fuente de los datos con enlace real
    st.markdown(
        '[Datos - Fincaraiz](https://www.fincaraiz.com.co)',
        unsafe_allow_html=True
    )
    st.markdown(
        '[API Colombia - Regiones](https://api-colombia.com)',
        unsafe_allow_html=True
    )
    

if filtro_terrenos:
    df = df[(df["habitaciones"]>0)& (df["baños"]>0) & (df["ciudades"] != "no especifica") & (df["region"] != "desconocido")]

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
with c1:
    st.metric(label=f"Mayor precio - {prop_mas_cara['ciudades']}", 
            value=f"${prop_mas_cara['precios']:,.0f}")

with c2:
    st.metric(label=f"Menor precio - {prop_men_cara['ciudades']}", 
            value=f"${prop_men_cara['precios']:,.0f}")

with c3:
    st.metric("Precio promedio", f"${df['precios'].mean():,.0f}")

with c4:
    st.metric("Total de propiedades", df.shape[0])
    

# _____________________ Visualizaciones __________________________________
st.subheader("Tabla de datos",divider="red")

# Mostramos el dataframe
st.dataframe(df,use_container_width=True,column_order=df_ordenado,hide_index=True)

# Mostramos las graficas
st.subheader("Graficas",divider="red")

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
    df_corr = df[variables].corr()
    # Heatmap con Plotly
    fig = px.imshow(df_corr,
                    text_auto=True,
                    color_continuous_scale='Viridis',
                    title="Matriz de Correlación")
    st.plotly_chart(fig)

# Regiones 
c1,c2 = st.columns(2)
with c1: 
    # Limitamos top a ≤ 7
    if top > 7:
        top = 6
    bar_fig_horizon = px.bar(top_regiones_caras, x="precios", y="region", 
                            orientation="h",text="precios",color="region",
                            title=f"Top {top} regiones con mayor precio promedio")
    
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
    
