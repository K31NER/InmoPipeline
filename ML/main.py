import logging
from ML.schema import Datainput
from ML.router import inmuebles
from fastapi_mcp import FastApiMCP
from ML.logger_config import logger_startup
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ML.utils import get_predict,load_model,get_distinct_city

# Connfiguramos el logger
logger_startup()

logger = logging.getLogger(__name__)

# Definimos el objeto de fastapi
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
    
    # Cargamos el modelo y su informacion
    model,model_data = load_model()
    
    #cargamos las ciudades distintas
    ciudades = get_distinct_city()
    app.state.ciudades = ciudades
    
    # validamos que se carge
    if not model:
        logger.error("No se logro cargar el modelo")
        raise RuntimeError("❌ Error al cargar el modelo")
    
    print("Modelo cargado con exito ✅")
    logger.info("Modelo cargado con exito")
        

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
        logger.exception("Error al realizar prediccion")
        raise HTTPException(404,detail="Error al ejecutar el modelo")
    
    logger.info("Prediccion realizada con exito")
    return JSONResponse(content={
        "Prediccion": f"$ {precio_estimado:,.2f} COP",
        "Datos Recibidos": data.model_dump(),
        "Details": model_data
    }, status_code=200)


# Incluimos los routers
app.include_router(inmuebles.router)

# definimos el server mcp
mcp = FastApiMCP(fastapi=app,
                describe_full_response_schema="Servidor MCP para realizar consultas sobre inmubeles en colombia")

# Montamos el servidor
mcp.mount()