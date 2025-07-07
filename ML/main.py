from schema import Datainput
from utils import get_predict,load_model
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API InmoPipeline",
    version="0.1",
    summary="Expone el modelo de machine learning para predicción de precios inmobiliarios",
)

# Definimos las urls que tendran acceso a la api
origins = [
    "http://localhost:8501","*"
]

# Agregamos los corns para indicar que streamlit puede realizar solicitudes
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods= ["*"],
    allow_headers = ["*"]
)

# Cargamos el modelo en el servidor
@app.on_event("startup")
def start_event():
    global model,model_data
    model,model_data = load_model()
    if model:
        print("Modelo cargado con exito ✅")
    if not model:
        raise RuntimeError("❌ Error al cargar el modelo")

# Endpoint de incio
@app.get("/")
async def index():
    return JSONResponse(content={"Message": "✅ Servidor iniciado con éxito - InmoPipeline API",
    "info": model_data},status_code=200)
    
# Endpoint para cargar el modelo
@app.post("/model")
async def run_model(data: Datainput):
    """
    Endpoint que recibe los datos de entrada y devuelve la predicción de precio.
    """
    try:
        precio_estimado = get_predict(data.m2, data.habs,
                                    data.baños, data.region,
                                    model)
    except Exception as e:
        print(e)
        raise HTTPException(404,detail="Error al ejecutar el modelo")
    
    return JSONResponse(content={
        "Prediccion": f"$ {precio_estimado:,.2f} COP",
        "Datos Recibidos": data.model_dump(),
        "Details": model_data
    }, status_code=200)