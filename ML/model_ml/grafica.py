import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import r2_score

# Cargar datos
df = pd.read_csv("Data/porcentaje_error.csv")

# Datos reales y predichos
y_true = df["real_price"]
y_pred = df["predict_price"]

# Métricas reales del modelo
r2 = r2_score(y_true, y_pred)
error_promedio = df["porcentaje_error"].mean()
n_datos = len(df)

# Crear figura base
fig = px.scatter(
    df,
    x="real_price",
    y="predict_price",
    title="Comparación entre Precio Real y Precio Predicho (Random Forest)",
    labels={"real_price": "Precio real", "predict_price": "Precio predicho"},
    log_x=True,
    log_y=True,
    color_discrete_sequence=["#1f77b4"],
    hover_data={"porcentaje_error": True}
)

# Línea de referencia ideal (y = x)
fig.add_trace(go.Scatter(
    x=y_true,
    y=y_true,
    mode='lines',
    line=dict(color='green', dash='dash'),
    name='Línea ideal (y = x)'
))

# Anotación con métricas reales
fig.add_annotation(
    text=f"<b>Error promedio:</b> {error_promedio:.2f}%<br>"
         f"<b>R² real:</b> {r2:.2f}<br>"
         f"<b>Datos:</b> {n_datos}",
    xref="paper", yref="paper",
    x=0.95, y=0.05,
    showarrow=False,
    bordercolor="black",
    borderwidth=1,
    bgcolor="white",
    font=dict(size=12)
)

# Mostrar
fig.show()
