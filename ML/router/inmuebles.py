import logging
from sqlmodel import text
from ML.db import connection
from fastapi.responses import JSONResponse
from ML.utils import normalizar_texto, regiones_map
from fastapi import APIRouter, HTTPException,Request

# Definimos el onjeto router
router = APIRouter(tags=["Datos"])

#Definimos le logger
logger = logging.getLogger(__name__)

# Definimos la consulta base
query_base = "SELECT ciudades,region,precios,habitaciones,baños,metros_cuadrados,enlaces FROM propiedades "

def ejecutar_consulta(db: connection, 
                    descripcion: str, 
                    filtros:list,
                    params: dict):
    """ Funcion para ejecutar las consultas en base a sus filtros 
    
    Parametros:
    
    - db: Conexion con la base de datos
    - descripcion: Pequeña anotacion del tipo de consulta
    - filtros: Lista de filtros
    - params: Dicionario de parametros
    
    Return:
    
    - JSONResponse: objeto json con la informa relevante de la consulta
    """
    
    where_clause = " WHERE " + " AND ".join(filtros) if filtros else ""
    limit_clause = " LIMIT :limit" if "limit" in params else ""
    
    query_sql = f"{query_base}{where_clause}{limit_clause}"
    
    logger.info(f"[{descripcion}] Ejecutando consulta con filtros: {filtros} | Parametros: {params}")
    
    try:
        query = text(query_sql)
        resultado = db.exec(query.params(**params))
        rows = resultado.fetchall()
        datos = [dict(row._mapping) for row in rows]
    except Exception:
        logger.exception(f"[{descripcion}] Error al ejecutar consulta")
        raise HTTPException(status_code=400, detail=f"Error al realizar consulta")
    
    logger.info(f"[{descripcion}] Consulta exitosa. Registros encontrados: {len(datos)}")
    
    return JSONResponse(content={
        "size": len(datos),
        "filtros": params,
        "data": datos,
    }, status_code=200)

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
        logger.warning(f"Region {region} no encontrada")
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
    
    # Validamos los limites
    if limite:
        params["limit"] = limite
        
    return ejecutar_consulta(db,f"Consulta por region {region_map}",filtros,params)



@router.get("/propiedades_ciudad/{ciudad}",
            summary="Retorna todos los datos de los inmubeles de esa ciudad")
def get_propiedades_by_ciudad(db:connection,
                            ciudad:str,
                            request: Request,
                            habs:int = None,
                            baños: int = None,
                            precio: int = None,
                            metros: int = None, 
                            limite:int = None,):
    
    # Creamos una lista y un diccionario para menajar los parametros
    filtros = []
    params = {}
    
    # Obtenemos las ciudades unicas de la base de datos
    ciudades = request.app.state.ciudades 
    
    # Validamos la ciudad
    ciudad_normalizada = ciudad.strip().lower()
    if ciudad_normalizada not in ciudades:
        logger.warning(f"Ciudad: {ciudad} no encontrada")
        raise HTTPException(status_code=404,
                        detail={"details":"Ciudad no encontradas"})
        
    # Agregamos la condicion principal
    filtros.append("ciudad_normalizada = :ciudad")
    params["ciudad"] = normalizar_texto(ciudad_normalizada)
    
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
        filtros.append("CAST(metros_cuadrados AS INTEGER) >= :metros")
        params["metros"] = metros
    
    if limite:
        params["limit"] = limite
        
    return ejecutar_consulta(db,f"Consulta por ciudad: {ciudad}",filtros,params)