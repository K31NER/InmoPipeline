import requests 
import pandas as pd

# Definimos las URLs
URL_BASE = "https://api-colombia.com/api/v1/"
URL_REGIONES = f"{URL_BASE}Region"
URL_DEPARTAMENTOS = f"{URL_BASE}Department/search/"

def get_regiones() -> dict:
    """ obtiene las regiones de colombia 
    --
    Return:
    - data: regiones 
    """
    
    resp = requests.get(URL_REGIONES)
    if resp.status_code == 200:
        json_data = resp.json()
        data = [{"id":j["id"],"region":j["name"]} for j in json_data]
        if not data:
            return {"message": "Error al obtener las regiones"}
        
        return  data
    
def get_region_by_city(ciudad: str, path_csv=False) -> str:
    """ Recibe el nombre de una ciudad y devuelve su respectiva region
    --
    Parametros:
    - ciudad = Nombre de la ciudad -> str
    - path_csv = Ruta del csv -> /data/mis_regiones.csv
    
    Return:
    - region = Devuelve la region de esa ciudad
    """
    try:
        if path_csv == False:
            regiones = get_regiones()
            df_regiones = pd.DataFrame(regiones)
        else:
            df_regiones = pd.read_csv(path_csv)
        
        resp = requests.get(f"{URL_DEPARTAMENTOS}{ciudad}")
        if resp.status_code == 200:
            json_data = resp.json()
            if json_data and len(json_data) > 0:
                region_id = json_data[0]["regionId"]
                
                region_ciudad = df_regiones[df_regiones["id"] == region_id]
                if not region_ciudad.empty:
                    return region_ciudad["region"].iloc[0]
    except Exception as e:
        return "desconocido"


if __name__ == "__main__":
    #data = get_regiones()
    #print(data)
    #df = pd.DataFrame(data)
    #df.to_csv("Data/regiones_colombia.csv",index=False,encoding="utf-8")
    cartagena_region = get_region_by_city("cartagena")
    print(cartagena_region)