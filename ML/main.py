from fastapi import FastAPI
from schema import Testinput
from fastapi.responses import JSONResponse

app = FastAPI(
    title="API InmoPipeline",
    version="0.1",
    summary="Expone el modelo de machine learning para predicción de precios inmobiliarios",
)

@app.get("/")
async def index():
    return {"Message": "✅ Servidor iniciado con éxito - InmoPipeline API"}
    
    
@app.post("/model")
async def run_model(data: Testinput):
    """
    Endpoint que recibe los datos de entrada y devuelve la predicción de precio.
    """
    
    # 🔮 Aquí en el futuro deberías cargar y usar tu modelo real:
    # precio_estimado = modelo.predict([data.habs, data.baños, data.m2, data.region])
    
    # Mientras tanto, respuesta de ejemplo:
    precio_estimado = "1.000M COP (estimado ficticio)"
    
    return JSONResponse(content={
        "Prediccion": precio_estimado,
        "Datos Recibidos": data.model_dump()
    }, status_code=200)