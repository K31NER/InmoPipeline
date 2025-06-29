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

def ver_corr(df:pd.DataFrame):
    pass

# Definimos el sidebar
with st.sidebar:
    st.image("https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-YxKlwIcjJqTAeRHzfEN0Qra6tvwzNQ.png&w=1920&q=75")
    st.subheader("Configuraciones")
    
    top = int(st.number_input(label="Digite el numero de top a mostrar",
                        value=5, min_value=3, max_value=10, step=1, format="%d", icon="🏆",help="Limita el numero de resultados mayores"))
    
    # Check para filtrar terrenos sin habitaciones ni baños
    filtro_terrenos = st.checkbox("Excluir terrenos",help="Elimina los inmuebles con habitaciones y baños con 0")
    
    generar_correlacions = st.button("ver correlaciones")
    
    # Fuente de los datos con enlace real
    st.markdown(
        '[Fuente de los datos](https://www.fincaraiz.com.co)',
        unsafe_allow_html=True
    )


# Cargamos el dataframe
df = pd.read_csv("../Data/propiedades.csv")

# Limpiamos el campo de ciudades
df["ciudades"] = df["ciudades"].str.lower()

df_ordenado = ["ciudades","precios","habitaciones","baños","metros_cuadrados","enlaces"]

if filtro_terrenos:
    df = df[(df["habitaciones"]>0)& (df["baños"]>0)]

# Fila de la propiedad más cara y mas barata
prop_mas_cara = df.loc[df["precios"].idxmax()]
prop_men_cara = df.loc[df["precios"].idxmin()]

# Definimos las agrupaciones

# Agrupacion por habitaciones
agrupacion_hab = df.groupby("habitaciones")["precios"].mean().reset_index()
top_hab = agrupacion_hab.nlargest(top,"precios")

# Agrupacion por ciudad
agrupacion_ciudad = df.groupby("ciudades")["precios"].mean().reset_index()
top_ciudades = agrupacion_ciudad.nlargest(top,"precios")

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

# Definimos el titulo y la tabla con los datos
st.title("Datos recopilados de FincaRaiz 🌐")


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
    
    
st.subheader("Tabla de datos")
# Mostramos el dataframe
st.dataframe(df,use_container_width=True,column_order=df_ordenado,hide_index=True)

c1,c2 = st.columns(2)
with c1: 
    variables = ["precios","metros_cuadrados","habitaciones","baños"]
    df_corr = df[variables].corr()
    
    # Heatmap con Plotly
    fig = px.imshow(df_corr,
                    text_auto=True,
                    color_continuous_scale='Viridis',
                    title="Matriz de Correlación")

    st.plotly_chart(fig)
with c2:
    st.subheader("Resumen de ciudades")
    st.dataframe(top_resumen_ciudades,use_container_width=True,hide_index=True)

# Mostramos las graficas
st.subheader("Graficas",divider="red")
c1,c2 = st.columns([2,4])
with c1:
    bar_fig = px.bar(top_hab,x="habitaciones",y="precios",text="precios",
                    title="Precio promedio segun habitaciones",color="habitaciones",)
    bar_fig.update_yaxes(type="log")
    
    
    st.plotly_chart(bar_fig)
with c2:
    bar_fig_horizon = px.bar(top_ciudades, x="precios", y="ciudades", 
                            orientation="h",text="precios",color="ciudades",
                            title="Top 5 ciudades con mayor precio promedio")
    
    st.plotly_chart(bar_fig_horizon)
    
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
    