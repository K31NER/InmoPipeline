import pandas as pd
import streamlit as st 

# Configuramos el dashboard
st.set_page_config(
    page_icon="https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-6F0Oea8suMLdEi6BoluXYbqXxnWEdt.png&w=1920&q=75",
    page_title="InmoPipeline",
    layout="wide"
)

# Cargamos el dataframe
df = pd.read_csv("../Data/propiedades.csv")
df_ordenado = ["ciudades","precios","habitaciones","baños","metros_cuadrados","enlaces"]

# Definimos las agrupaciones
agrupacion_hab = df.groupby("habitaciones")["precios"].mean().reset_index()
agrupacion_ciudad = df.groupby("ciudades")["precios"].mean().reset_index()
top_ciudades = agrupacion_ciudad.sort_values("precios", ascending=False).head(5)


# Definimos el sidebar
with st.sidebar:
    st.image("https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-YxKlwIcjJqTAeRHzfEN0Qra6tvwzNQ.png&w=1920&q=75")
    st.subheader("Configuraciones")
    
    # Fuente de los datos con enlace real
    st.markdown(
        '[Fuente de los datos](https://www.fincaraiz.com.co)',
        unsafe_allow_html=True
    )

# Definimos el titulo y la tabla con los datos
st.title("Datos recopilados de FincaRaiz 🌐")

# Definimos las metricas importantes
c1,c2,c3,c4 = st.columns(4)
with c1:
    st.metric("Mayor precio", f"${df['precios'].max():,.0f}")

with c2:
    st.metric("Menor precio", f"${df['precios'].min():,.0f}")

with c3:
    st.metric("Precio promedio", f"${df['precios'].mean():,.0f}")

with c4:
    st.metric("Total de propiedades", df.shape[0])
    
# Mostramos el dataframe
st.dataframe(df,use_container_width=True,column_order=df_ordenado,hide_index=True)


# Mostramos las graficas
st.subheader("Graficas",divider="red")
c1,c2 = st.columns(2)
with c1:
    st.subheader("Relación número de habitaciones vs. precio promedio")
    st.bar_chart(agrupacion_hab,x="habitaciones",y="precios",color="precios")
with c2:
    st.subheader("Top 5 ciudades con mayor precio promedio")
    st.bar_chart(top_ciudades,x="ciudades",y="precios",color="ciudades",horizontal=True,height=400)