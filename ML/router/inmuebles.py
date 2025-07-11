from typing import Optional
import unicodedata
from sqlmodel import text
from ML.db import connection
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Datos"])

# Definimos la consulta base
query_base = "SELECT ciudades,region,precios,habitaciones,baños,metros_cuadrados,enlaces FROM propiedades "

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

@router.get("/propiedades_region/{region}",summary="Retorna todos los datos de los inmuebles en esa region")
def get_propiedades_by_region(db:connection,
                            region:str,
                            habs:int = None,
                            baños: int = None,
                            precio:int = None,
                            metros:int = None,
                            limite:int = None
                            ):
    
    # Creamos una lista y un diccionario para menajar los parametros
    filtros = []
    params = {}
    
    #limpiamos la region
    region_normalizada = normalizar_texto(region)
    region_map = regiones_map.get(region_normalizada)
    
    if not region_map:
        raise HTTPException(status_code=404,
                        detail={"details":f"Region {region} no encontrada",
                                "Lista de regiones": list(regiones_map.keys())})
        
    # Agregamos el filtro principal
    filtros.append("region = :region")
    params["region"] = region_map
    
    # Validamos las habitaciones
    if habs:
        filtros.append("CAST(habitaciones AS INTEGER) = :habs")
        params["habs"] = habs
    
    # Validamos si hay baños
    if baños:
        filtros.append("CAST(baños AS INTEGER) = :baños")
        params["baños"] = baños
    
    # Validamos si hay precios
    if precio:
        filtros.append("CAST(precios AS INTEGER) >= :precio")
        params["precio"] = precio
        
    # Validamos si hay metros
    if metros:
        filtros.append("CAST(metros_cuadrados AS INTEGER) >= :metros")
        params["metros"] = metros
        
    # Definimos el filtro where
    where_clause = " WHERE " + " AND ".join(filtros) if filtros else ""
    
    # Definimos el limitador
    limit_clause = " LIMIT :limit" if limite else ""
    
    # Validamos los limites
    if limite:
        params["limit"] = limite
        
    try:
        query = text(f"{query_base}{where_clause}{limit_clause}")
        resultado = db.exec(query.params(**params))
        
        rows = resultado.fetchall()
        datos = [dict(row._mapping) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al realizar consulta: {e}")
    
    return JSONResponse(content={
        "size": len(datos),
        "filtro": params,
        "data": datos,
    },status_code=200)


@router.get("/propiedades_ciudad/{ciudad}",
            summary="Retorna todos los datos de los inmubeles de esa ciudad")
def get_propiedades_by_ciudad(db:connection,
                            ciudad:str,
                            habs:int = None,
                            baños: int = None,
                            precio: int = None,
                            metros: int = None, 
                            limite:int = None):
    
    # Creamos una lista y un diccionario para menajar los parametros
    
    filtros = []
    params = {}
    
    # Validamos la ciudad
    if not ciudad:
        raise HTTPException(status_code=404,
                        detail={"details":f"Ciudades no encontradas"})
        
    # Agregamos la condicion principal
    filtros.append("ciudad_normalizada = :ciudad")
    params["ciudad"] = normalizar_texto(ciudad)
    
    # Validamos las habitaciones
    if habs:
        filtros.append("CAST(habitaciones AS INTEGER) = :habs")
        params["habs"] = habs
    
    # Validamos si esta el campo baños
    if baños:
        filtros.append("CAST(baños AS INTEGER) = :baños")
        params["baños"] = baños
        
    # Validamos si esta el campo precio
    if precio:
        filtros.append("CAST(precios AS INTEGER) >= :precio")
        params["precio"] = precio
    
    # Validamos si esta el campo metros
    if metros:
        filtros.append("CAST(metros_cuadrados AS INTEGER) >= :metro")
        params["metro"] = metros
    
    # Creamos las consultas
    where_clause = " WHERE " + " AND ".join(filtros) if filtros else ""
    limit_clause = " LIMIT :limit" if limite else ""
    
    if limite:
        params["limit"] = limite
        
    try:
        query = text(f"{query_base}{where_clause}{limit_clause}")
        resultado = db.exec(query.params(**params))
        
        rows = resultado.fetchall()
        datos = [dict(row._mapping) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al realizar consulta: {e}")
    
    return JSONResponse(content={
        "size": len(datos),
        "filtros":params,
        "data": datos,
    },status_code=200)