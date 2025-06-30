import pandas as pd
from Region import get_region_by_city

CSV_REGIONES = "Data/regiones_colombia.csv"

def add_regiones(df):
    # Asignamos las regiones
    ciudades_unicas = df["ciudades"].unique() # sacamos las ciudades unicas
    
    # Obtenemos las regiones de cada ciudad
    region_map = {ciu: get_region_by_city(ciu,path_csv=CSV_REGIONES) for ciu in ciudades_unicas}
    
    # Creamos las columnas de regiones
    df["region"] = df["ciudades"].map(region_map).fillna("desconocido")
    
    return df
    
# Función corregida para extraer ciudad
def extraer_ciudad(texto):
    # Busca la última aparición de "en" y captura lo que viene después
    partes = texto.split(" en ")
    if len(partes) > 1:
        # Lo que viene después del último "en" es lo que nos interesa
        ciudad = partes[-1].strip()
        return ciudad
    elif texto.strip() and len(texto.strip().split()) <= 2:
        # Si es una palabra o dos y no contiene "apartamento", "venta", etc., asumimos que es la ciudad
        return texto.strip()
    else:
        return 'no especifica'
    
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """ Obtiene las ciudades y limpia el campo de precio"""
    
    # Obtenemos solo la ciudad
    df["ciudades"] = df["titulos"].str.split(",").str[-1].str.strip()
    
    # Limpiamos el precio
    df["precios"] = (
        df["precios"]
        .str.replace("Desde", "", regex=False)
        .str.replace(r"[$\.]", "", regex=True)
        .str.strip()
    )
    
    # Volvemos el precio un valor numerico
    df["precios"] = pd.to_numeric(df["precios"],errors="coerce")
    
    # Limpiamos las ciudades
    df["ciudades"] = df["ciudades"].str.lower()
    df["ciudades"] = df["ciudades"].apply(extraer_ciudad)
    
    return df

if __name__ == "__main__":
    #df = pd.read_csv("Data/propiedades.csv")
    #df_limpio = clean_data(df)
    #print(df["metros_cuadrados"].head())
    pass
