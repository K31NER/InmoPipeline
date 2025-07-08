import unicodedata
from sqlmodel import text
from ML.db import connection
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Datos"])

# Definimos la consulta base
query_base = "SELECT ciudad_normalizada,region,precios,habitaciones,baños,metros_cuadrados,enlaces FROM propiedades "

# Diccionario para mapear entrada normalizada a nombre correcto
regiones_map = {
    "caribe": "Caribe",
    "amazonia": "Amazonia",
    "pacifico": "Pacífico",
    "orinoquia": "Orinoquía",
    "andina": "Andina",
    "insular": "Insular",
    "desconocido": "desconocido"
}

def normalizar_texto(texto: str) -> str:
    # Elimina tildes y pone en minúsculas
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()

@router.get("/data_by_region/{region}",summary="Retorna todos los datos de los inmuebles en esa region")
def get_data(db:connection,region:str,limite:int = None):
    
    #limpiamos la region
    region_normalizada = normalizar_texto(region)
    region_map = regiones_map.get(region_normalizada)
    
    if not region_map:
        raise HTTPException(status_code=404,
                        detail={"details":f"Region {region} no encontrada",
                                "Lista de regiones": list(regiones_map.keys())})
        
    try:
        query = text(f"{query_base} WHERE region = :region LIMIT :limite")
        resultado = db.exec(query.params(region = region_map,limite = limite))
        
        rows = resultado.fetchall()
        datos = [dict(row._mapping) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al realizar consulta: {e}")
    
    return JSONResponse(content={
        "size": len(datos),
        "region":region_map,
        "data": datos,
    },status_code=200)

@router.get("/data_by_ciudad/{ciudad}",
            summary="Retorna todos los datos de los inmubeles de esa ciudad")
def get_data(db:connection,ciudad:str,limite:int = None):
        
    if not ciudad:
        raise HTTPException(status_code=404,
                        detail={"details":f"Ciudades no encontradas"})
        
    try:
        query = text(f"{query_base} WHERE ciudad_normalizada = :ciudad LIMIT :limite")
        resultado = db.exec(query.params(ciudad = normalizar_texto(ciudad),limite = limite))
        
        rows = resultado.fetchall()
        datos = [dict(row._mapping) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al realizar consulta: {e}")
    
    return JSONResponse(content={
        "size": len(datos),
        "ciudades":ciudad,
        "data": datos,
    },status_code=200)